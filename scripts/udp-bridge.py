#!/usr/bin/env python3
"""udp-bridge.py - carry UDP datagrams through a TCP connection, such as an SSH tunnel.

SSH forwards TCP only. This tool wraps each UDP datagram in a small frame, sends the frames
over ONE TCP connection, and unwraps them on the far side. Datagram boundaries are preserved,
and many UDP clients share the single connection.

  players --UDP--> [entry] --TCP, inside the SSH tunnel--> [exit] --UDP--> game server

  entry  runs on the relay host that players can reach. It listens for UDP and connects out
         to a LOCAL TCP port (the near end of the SSH reverse tunnel).
  exit   runs at home. It listens on a local TCP port (the far end of the tunnel) and sends
         the datagrams on to the game server.

Usage
  udp-bridge.py entry --udp 0.0.0.0:5520 --tunnel 127.0.0.1:15520 [--allow CIDR ...]
  udp-bridge.py exit  --tunnel-listen 127.0.0.1:15520 --target <game-host>:5520

Known limit: a burst of a few hundred datagrams sent in the same instant can overflow the UDP
socket buffer and lose a few. Real game traffic is paced, so this does not matter in practice;
udp-probe.py's --interval 0 mode is a deliberate stress test, so keep its --count modest.

Frame: type (1 byte, 0 = data, 1 = close), session id (2 bytes), payload length (2 bytes),
all big-endian, then the payload. Standard library only (Python 3.8+).
"""
import argparse, asyncio, ipaddress, logging, socket, struct, sys, time

HEADER = struct.Struct("!BHH")
DATA, CLOSE = 0, 1
MAX_BUFFER = 256 * 1024          # bytes queued toward the tunnel before new datagrams are dropped
log = logging.getLogger("udp-bridge")


def split_hostport(text):
    host, _, port = text.rpartition(":")
    if not host or not port.isdigit():
        raise argparse.ArgumentTypeError(f"expected HOST:PORT, got {text!r}")
    return host, int(port)


def set_nodelay(writer):
    sock = writer.get_extra_info("socket")
    if sock is not None:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)


def frame(kind, sid, payload=b""):
    return HEADER.pack(kind, sid, len(payload)) + payload


def congested(writer):
    return writer.transport.get_write_buffer_size() > MAX_BUFFER


async def read_frame(reader):
    kind, sid, length = HEADER.unpack(await reader.readexactly(HEADER.size))
    payload = await reader.readexactly(length) if length else b""
    return kind, sid, payload


# ----------------------------------------------------------------------------- entry
class EntryUDP(asyncio.DatagramProtocol):
    def __init__(self, owner):
        self.owner = owner

    def connection_made(self, transport):
        self.owner.udp = transport

    def datagram_received(self, data, addr):
        self.owner.from_player(data, addr)


class Entry:
    def __init__(self, a):
        self.a = a
        self.writer = None
        self.udp = None
        self.by_addr, self.by_sid = {}, {}       # addr -> sid ; sid -> [addr, last_seen]
        self.sent = self.received = self.dropped = 0
        self.warned = {}                          # reason -> time of the last warning
        self.nets = [ipaddress.ip_network(c, strict=False) for c in (a.allow or [])]

    def warn_once(self, reason, text):
        now = time.monotonic()
        if now - self.warned.get(reason, -1e9) > 10:
            self.warned[reason] = now
            log.warning(text)

    def from_player(self, data, addr):
        if self.nets and not any(ipaddress.ip_address(addr[0]) in n for n in self.nets):
            self.dropped += 1; return
        w = self.writer
        if w is None or w.is_closing():
            self.dropped += 1; return
        if congested(w):
            self.dropped += 1
            self.warn_once("congested", "tunnel is congested; dropping datagrams (the link to the relay is slower than the traffic)")
            return
        key = addr[:2]
        sid = self.by_addr.get(key)
        if sid is None:
            if len(self.by_sid) >= self.a.max_sessions:
                self.dropped += 1
                self.warn_once("cap", f"session limit ({self.a.max_sessions}) reached; dropping new players until sessions go idle")
                return
            sid = next(i for i in range(1, 65536) if i not in self.by_sid)
            self.by_addr[key] = sid
            self.by_sid[sid] = [key, time.monotonic()]
            log.info("new session %d for %s:%d", sid, *key)
        self.by_sid[sid][1] = time.monotonic()
        w.write(frame(DATA, sid, data))
        self.sent += 1

    def forget(self, sid, notify=True):
        info = self.by_sid.pop(sid, None)
        if info:
            self.by_addr.pop(info[0], None)
            if notify and self.writer and not self.writer.is_closing():
                self.writer.write(frame(CLOSE, sid))

    async def tunnel_loop(self):
        host, port = self.a.tunnel
        while True:
            try:
                reader, writer = await asyncio.open_connection(host, port)
                set_nodelay(writer)
                self.writer = writer
                log.info("tunnel connected (%s:%d)", host, port)
                while True:
                    kind, sid, payload = await read_frame(reader)
                    info = self.by_sid.get(sid)
                    if kind == DATA and info:
                        info[1] = time.monotonic()
                        self.udp.sendto(payload, info[0])
                        self.received += 1
                    elif kind == CLOSE:
                        self.forget(sid, notify=False)
            except (OSError, asyncio.IncompleteReadError) as e:
                log.warning("tunnel down (%s); retrying in 2 s", e.__class__.__name__)
            finally:
                self.writer = None
                self.by_addr.clear(); self.by_sid.clear()
            await asyncio.sleep(2)

    async def housekeeping(self):
        while True:
            await asyncio.sleep(10)
            now = time.monotonic()
            for sid in [s for s, (_, t) in self.by_sid.items() if now - t > self.a.idle]:
                log.info("session %d idle, closing", sid)
                self.forget(sid)
            log.info("sessions %d  to tunnel %d  from tunnel %d  dropped %d",
                     len(self.by_sid), self.sent, self.received, self.dropped)

    async def run(self):
        loop = asyncio.get_running_loop()
        await loop.create_datagram_endpoint(lambda: EntryUDP(self), local_addr=self.a.udp)
        log.info("entry listening on UDP %s:%d", *self.a.udp)
        await asyncio.gather(self.tunnel_loop(), self.housekeeping())


# ------------------------------------------------------------------------------ exit
class ExitUDP(asyncio.DatagramProtocol):
    def __init__(self, sid, writer, touch):
        self.sid, self.writer, self.touch = sid, writer, touch

    def datagram_received(self, data, addr):
        self.touch(self.sid)
        if not self.writer.is_closing() and not congested(self.writer):
            self.writer.write(frame(DATA, self.sid, data))

    def error_received(self, exc):
        log.debug("target error: %s", exc)


class Exit:
    def __init__(self, a):
        self.a = a
        self.current = None

    async def handle(self, reader, writer):
        if self.current and not self.current.is_closing():
            log.info("replacing the previous tunnel connection")
            self.current.close()
        self.current = writer
        set_nodelay(writer)
        log.info("tunnel connection from the entry side")
        loop = asyncio.get_running_loop()
        sessions = {}                              # sid -> [transport, last_seen]

        def touch(sid):
            if sid in sessions:
                sessions[sid][1] = time.monotonic()

        async def reaper():
            while True:
                await asyncio.sleep(10)
                now = time.monotonic()
                for sid in [s for s, (_, t) in sessions.items() if now - t > self.a.idle]:
                    sessions.pop(sid)[0].close()
                    if not writer.is_closing():
                        writer.write(frame(CLOSE, sid))

        task = asyncio.create_task(reaper())
        try:
            while True:
                kind, sid, payload = await read_frame(reader)
                if kind == DATA:
                    s = sessions.get(sid)
                    if s is None:
                        if len(sessions) >= self.a.max_sessions:
                            continue
                        transport, _ = await loop.create_datagram_endpoint(
                            lambda sid=sid: ExitUDP(sid, writer, touch), remote_addr=self.a.target)
                        s = sessions[sid] = [transport, time.monotonic()]
                    s[0].sendto(payload)
                    s[1] = time.monotonic()
                elif kind == CLOSE and sid in sessions:
                    sessions.pop(sid)[0].close()
        except (asyncio.IncompleteReadError, ConnectionError):
            pass
        finally:
            task.cancel()
            for t, _ in sessions.values():
                t.close()
            writer.close()
            log.info("tunnel connection closed")

    async def run(self):
        host, port = self.a.tunnel_listen
        if host not in ("127.0.0.1", "::1", "localhost"):
            log.warning("listening on %s is not loopback: anyone who can reach it can send UDP to the target", host)
        server = await asyncio.start_server(self.handle, host, port)
        log.info("exit waiting for the tunnel on TCP %s:%d, forwarding UDP to %s:%d", host, port, *self.a.target)
        async with server:
            await server.serve_forever()


# ------------------------------------------------------------------------------ main
def main():
    p = argparse.ArgumentParser(description="UDP-over-TCP bridge for SSH tunnels")
    sub = p.add_subparsers(dest="mode", required=True)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--max-sessions", type=int, default=64, help="most simultaneous UDP clients (default 64)")
    common.add_argument("--idle", type=float, default=60, help="seconds before an idle session closes (default 60)")
    common.add_argument("-v", "--verbose", action="store_true")
    e = sub.add_parser("entry", parents=[common])
    e.add_argument("--udp", type=split_hostport, required=True, help="HOST:PORT to receive player UDP on")
    e.add_argument("--tunnel", type=split_hostport, required=True, help="HOST:PORT of the local tunnel end")
    e.add_argument("--allow", action="append", metavar="CIDR", help="only accept players from these networks (repeatable)")
    x = sub.add_parser("exit", parents=[common])
    x.add_argument("--tunnel-listen", type=split_hostport, required=True, help="HOST:PORT to wait for the tunnel on")
    x.add_argument("--target", type=split_hostport, required=True, help="HOST:PORT of the UDP service")
    a = p.parse_args()
    logging.basicConfig(level=logging.DEBUG if a.verbose else logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
    try:
        asyncio.run((Entry if a.mode == "entry" else Exit)(a).run())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    sys.exit(main())

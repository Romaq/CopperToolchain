#!/usr/bin/env python3
"""udp-probe.py - prove that UDP really travels a path, and measure how well.

  server  echoes every datagram back to its sender.
  client  sends numbered datagrams, waits for the echoes, then reports loss, duplicates,
          reordering, damaged or resized datagrams, and round-trip time.
          Exit status: 0 = PASS, 1 = FAIL, 2 = usage error.

Examples
  udp-probe.py server --bind 0.0.0.0 --port 55520
  udp-probe.py client --host 127.0.0.1 --port 55520
  udp-probe.py client --host 127.0.0.1 --port 55520 --interval 0 --sizes 64,512,1200   # burst test

Why the burst test matters: a tunnel that carries UDP inside TCP must keep each datagram
separate. Sending many datagrams back to back, in different sizes, is how you find out whether
it does. Standard library only (Python 3.8+).
"""
import argparse, select, socket, statistics, struct, sys, time

MAGIC = b"UPRB"
HEAD = struct.Struct("!4sIQH")          # magic, sequence, send time (ns), total size
MIN_SIZE = HEAD.size


def make_packet(seq, size, t_ns):
    body = bytes((seq + i) & 0xFF for i in range(size - HEAD.size))
    return HEAD.pack(MAGIC, seq, t_ns, size) + body


def check_packet(data):
    """Return (seq, send_ns, problem). problem is None when the datagram is intact."""
    if len(data) < HEAD.size:
        return None, None, "too short"
    magic, seq, t_ns, size = HEAD.unpack_from(data)
    if magic != MAGIC:
        return None, None, "bad header"
    if len(data) != size:
        return seq, t_ns, f"size changed ({size} sent, {len(data)} received)"
    if data[HEAD.size:] != bytes((seq + i) & 0xFF for i in range(size - HEAD.size)):
        return seq, t_ns, "payload damaged"
    return seq, t_ns, None


def run_server(a):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((a.bind, a.port))
    if not a.quiet:
        print(f"echo server listening on UDP {a.bind}:{a.port} (Ctrl-C to stop)")
    n = 0
    try:
        while True:
            data, addr = s.recvfrom(65535)
            s.sendto(data, addr)
            n += 1
    except KeyboardInterrupt:
        pass
    if not a.quiet:
        print(f"echoed {n} datagrams")


def run_client(a):
    try:
        sizes = [int(x) for x in a.sizes.split(",")]
    except ValueError:
        print("--sizes must be a comma-separated list of integers", file=sys.stderr); return 2
    if any(x < MIN_SIZE or x > 65000 for x in sizes):
        print(f"each size must be between {MIN_SIZE} and 65000", file=sys.stderr); return 2

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setblocking(False)
    dest = (a.host, a.port)

    sent_at, rtts, seen = {}, [], set()
    bad, dup, reordered, highest = [], 0, 0, -1

    def drain(wait):
        nonlocal dup, reordered, highest
        end = time.monotonic() + wait
        while True:
            left = end - time.monotonic()
            r, _, _ = select.select([s], [], [], max(left, 0))
            if not r:
                return
            try:
                data, _ = s.recvfrom(65535)
            except BlockingIOError:
                return
            now = time.monotonic_ns()
            seq, t_ns, problem = check_packet(data)
            if problem:
                bad.append(problem); continue
            if seq in seen:
                dup += 1; continue
            seen.add(seq)
            if seq < highest:
                reordered += 1
            highest = max(highest, seq)
            rtts.append((now - t_ns) / 1e6)

    for seq in range(a.count):
        size = sizes[seq % len(sizes)]
        t = time.monotonic_ns()
        sent_at[seq] = t
        s.sendto(make_packet(seq, size, t), dest)
        drain(a.interval)                # waits `interval` seconds while collecting echoes
    drain(a.timeout)                     # grace period for stragglers

    got = len(seen)
    lost = a.count - got
    loss_pct = 100.0 * lost / a.count
    print(f"target            UDP {a.host}:{a.port}")
    print(f"sent              {a.count}   sizes {sizes}   interval {a.interval}s")
    print(f"received          {got}   lost {lost} ({loss_pct:.2f}%)   duplicates {dup}   out of order {reordered}")
    print(f"damaged/resized   {len(bad)}" + (f"   first problem: {bad[0]}" if bad else ""))
    if rtts:
        srt = sorted(rtts)
        p95 = srt[min(len(srt) - 1, int(len(srt) * 0.95))]
        jit = statistics.mean(abs(x - y) for x, y in zip(rtts, rtts[1:])) if len(rtts) > 1 else 0.0
        print(f"round trip (ms)   min {srt[0]:.2f}   median {statistics.median(srt):.2f}   "
              f"p95 {p95:.2f}   max {srt[-1]:.2f}   jitter {jit:.2f}")
    ok = got > 0 and not bad and loss_pct <= a.max_loss
    if got == 0 and not bad:
        print("no echoes came back: check the address and port, the firewall, and that the echo server is running")
    elif bad:
        print("some datagrams arrived merged, split, or altered: the path is not preserving datagram boundaries")
    print("RESULT            " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main():
    p = argparse.ArgumentParser(description="UDP echo server and verifying client")
    sub = p.add_subparsers(dest="mode", required=True)
    sv = sub.add_parser("server")
    sv.add_argument("--bind", default="0.0.0.0")
    sv.add_argument("--port", type=int, required=True)
    sv.add_argument("--quiet", action="store_true")
    cl = sub.add_parser("client")
    cl.add_argument("--host", required=True)
    cl.add_argument("--port", type=int, required=True)
    cl.add_argument("--count", type=int, default=200)
    cl.add_argument("--sizes", default="64,256,1200", help="comma-separated datagram sizes, cycled")
    cl.add_argument("--interval", type=float, default=0.02, help="seconds between sends; 0 = burst")
    cl.add_argument("--timeout", type=float, default=2.0, help="seconds to wait for late echoes")
    cl.add_argument("--max-loss", type=float, default=1.0, help="PASS threshold, percent")
    a = p.parse_args()
    if a.mode == "server":
        run_server(a); return 0
    return run_client(a)


if __name__ == "__main__":
    sys.exit(main())

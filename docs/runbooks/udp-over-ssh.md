# Runbook: carrying UDP through an SSH tunnel (workstream C)

Goal: let invited players reach a UDP game server at home that sits behind a network which allows
only outbound connections, through a relay host they can reach, and **prove** that it works.

Placeholders used below: `<RELAY>` the relay host, `<RELAY_USER>` the account on it, `<TUNNEL_PORT>`
a free TCP port number (for example 15520), `<GAME_HOST>` the machine at home running the game,
`<GAME_PORT>` the game's UDP port, `<KEY>` an SSH key file.

## 1. The idea in one minute

- SSH port forwarding (`-L`, `-R`) moves **TCP only**. It cannot forward UDP directly.
- The workaround is to put each UDP datagram into a small frame, send the frames through one TCP
  connection (which SSH can carry), and unwrap them at the other end. `scripts/udp-bridge.py` does this.
- The frames keep datagram boundaries intact. A plain byte pipe does not, and a game protocol breaks.
  `scripts/udp-probe.py` exists to catch exactly that.

The game in question, Hytale, uses QUIC over UDP on port 5520 by default and needs no TCP forwarding.

```
 player --UDP <GAME_PORT>--> [relay's gateway forwards the port]
                                  |
                           <RELAY>: udp-bridge ENTRY      (listens for UDP, dials the tunnel end)
                                  |  TCP 127.0.0.1:<TUNNEL_PORT>
                                  v  (inside the SSH reverse tunnel, opened FROM HOME)
        home: ssh -R ...  -->  udp-bridge EXIT  --UDP-->  <GAME_HOST>:<GAME_PORT>
```

## 2. Choosing an approach

| Approach | What it takes | Trade-offs |
|---|---|---|
| **UDP-over-TCP bridge through SSH (this runbook)** | Two scripts, an SSH reverse tunnel you already know, a forwarded UDP port on the relay's gateway | Quick, no root, no new software. Carries UDP inside TCP, so one lost packet on the home-to-relay path can delay the ones behind it. |
| **WireGuard to the relay** | WireGuard on both ends, one UDP port forwarded on the relay's gateway, a forwarding rule on the relay | Carries UDP natively, so it is the better long-term answer if the bridge feels laggy. More to set up on the relay side. |
| `ssh -w` (tun device) | Root on both ends, `PermitTunnel` on the relay | Still TCP underneath. More privileges than this job needs. |

Start with the bridge. Move to WireGuard if the verification results (section 5) or play feel poor.

## 3. Before touching the network: prove the tools work

    scripts/udp-selftest.sh

It runs everything on one machine, with an echo server standing in for the game and a plain local
TCP connection standing in for the SSH tunnel. Expect `SELF-TEST PASSED`. This also teaches what each
piece does, so read the script while it runs.

## 4. Setup

### Home side (the exit end)

1. Start the exit end. For the first tests, point it at the echo server instead of the game:

       scripts/udp-probe.py server --bind 127.0.0.1 --port 55520 --quiet &
       scripts/udp-bridge.py exit --tunnel-listen 127.0.0.1:<TUNNEL_PORT> --target 127.0.0.1:55520

2. In another terminal, open the reverse tunnel. Run it on the same machine as the exit end:

       ssh -N -T -i <KEY> \
           -o ExitOnForwardFailure=yes -o ServerAliveInterval=15 -o ServerAliveCountMax=3 \
           -R 127.0.0.1:<TUNNEL_PORT>:127.0.0.1:<TUNNEL_PORT> <RELAY_USER>@<RELAY>

   Because the relay side is bound to `127.0.0.1`, only programs on the relay itself can use the tunnel.

### Relay side (the entry end)

1. Give the relay account a dedicated key that can do nothing except open that one tunnel. In the
   relay account's `authorized_keys`, put this in front of the public key:

       restrict,port-forwarding,permitlisten="127.0.0.1:<TUNNEL_PORT>" <PUBLIC-KEY>

2. Copy `udp-bridge.py` (and `udp-probe.py` for testing) to the relay. Start the entry end:

       python3 udp-bridge.py entry --udp 0.0.0.0:<GAME_PORT> --tunnel 127.0.0.1:<TUNNEL_PORT>

   Optional: `--allow <CIDR>` (repeatable) limits which player networks it accepts.
3. On the relay's gateway, forward **UDP** `<GAME_PORT>` to the relay machine, and allow it in the relay's firewall.

## 5. Verification ladder

Climb one rung at a time. Do not move up until the rung below passes. A pass means `RESULT PASS`
from `udp-probe.py client`, which requires no damaged or resized datagrams and loss within 1%.

| Rung | Run this | What it proves |
|---|---|---|
| 1. Tunnel is up | On the relay: `ss -ltn` shows `<TUNNEL_PORT>`. At home: the exit end logs "tunnel connection". | SSH reverse tunnel and bridge ends are connected. |
| 2. Through the tunnel, from the relay itself | `udp-probe.py client --host 127.0.0.1 --port <GAME_PORT>` | The whole path works end to end, with the echo server as the target. |
| 3. Burst test | Same, adding `--interval 0 --count 120 --sizes 64,512,1200` | Datagram boundaries survive. |
| 4. From another machine on the relay's LAN | Same, with `--host <relay LAN address>` | The relay's firewall and listener are correct. |
| 5. From outside | A helper on a different network runs the client against the relay's public address | The gateway's UDP port forward works. This is the only reliable test: many online port checkers test TCP only. |
| 6. The real game | Stop the echo target, restart the exit end with `--target <GAME_HOST>:<GAME_PORT>`, and have one remote player join | The game itself works through the path. The entry end logs "new session". |

Read the numbers at rungs 2 to 5:

- **loss:** 1% or less is a pass. More than that means the path is dropping packets.
- **round trip:** compare the median with `ping -c 20 <RELAY>`. The tunnel should add roughly the
  home-to-relay delay and little else.
- **p95 versus median:** if p95 is more than about three times the median, expect rubber-banding. That
  pattern is the signature of TCP holding packets back, which is the case for moving to WireGuard.
- Remember the **upload speed** at home: every reply to every player leaves through it.

## 6. Keeping it running (next step, after the tests pass)

Run the SSH tunnel and the exit end as services so they restart on failure and at boot (for example
systemd units in a small container at home), and run the entry end the same way on the relay. The entry
end reconnects to the tunnel by itself every 2 seconds, so the order of starting does not matter.

## 7. Security notes

- The tunnel key can only open one forwarded port, and it is bound to the relay's loopback.
- The exit end listens on loopback only. Never change that to a public address.
- The game's own allow list still decides who may play. `--allow` adds a network-level limit.
- The tunnel adds no secrecy to the player-to-relay leg. QUIC encrypts game traffic itself.
- `--max-sessions` (default 64) and `--idle` (default 60 seconds) bound how much the entry end can be asked to hold.

## 8. Limits to know about

- Datagrams ride inside TCP, so a stall delays everything behind it.
- When the tunnel cannot keep up, the entry end drops datagrams rather than queueing them, and logs a warning.
- Bursts of a few hundred datagrams in the same instant can overflow the UDP socket buffer. Game traffic is
  paced, so this appears only in deliberate stress tests.

## 9. Troubleshooting

| Symptom | Check |
|---|---|
| Rung 2 prints "no echoes came back" | Is the tunnel up (rung 1)? Is the echo server running at home? Is the exit end pointed at it? |
| "some datagrams arrived merged, split, or altered" | The path is not preserving datagram boundaries. Something is acting as a plain byte pipe. |
| Rung 2 passes, rung 4 fails | The entry end is bound to `127.0.0.1` instead of `0.0.0.0`, or the relay's firewall blocks UDP `<GAME_PORT>`. |
| Rung 4 passes, rung 5 fails | The gateway forward is missing, is TCP instead of UDP, or points at the wrong machine. |
| Entry log says "tunnel down" repeatedly | The SSH tunnel is not running, or the exit end is not listening on `<TUNNEL_PORT>`. |
| Entry log says "session limit reached" | Many short-lived clients are holding sessions. Wait for `--idle`, or raise `--max-sessions`. |
| Everything passes but play is laggy | See the p95 note in section 5, and consider WireGuard. |

## 10. Done means

- [ ] `udp-selftest.sh` passes on the machine that runs it.
- [ ] Rungs 1 to 5 pass, with the numbers recorded in a decision record in `docs/decisions/`.
- [ ] A real player from outside joins the hosted game (rung 6).
- [ ] The tunnel, exit end, and entry end restart by themselves.
- [ ] The setup is written up in `docs/` so someone else could repeat it.

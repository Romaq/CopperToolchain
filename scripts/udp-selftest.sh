#!/usr/bin/env bash
# udp-selftest.sh - prove the UDP bridge works, using only this machine (no SSH, no network).
#
# It starts: an echo server (standing in for the game), the bridge "exit" and "entry" ends joined
# by a plain local TCP connection (standing in for the SSH tunnel), then runs the probe through it.
# Usage: scripts/udp-selftest.sh      Exit status 0 = every test passed.
set -uo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ECHO=55520; TUNNEL=55521; ENTRY=55522
pids=()
cleanup() { for p in "${pids[@]}"; do kill "$p" 2>/dev/null; done; wait 2>/dev/null; }
trap cleanup EXIT

python3 "$here/udp-probe.py" server --bind 127.0.0.1 --port $ECHO --quiet & pids+=($!)
python3 "$here/udp-bridge.py" exit  --tunnel-listen 127.0.0.1:$TUNNEL --target 127.0.0.1:$ECHO >/dev/null 2>&1 & pids+=($!)
sleep 0.5
python3 "$here/udp-bridge.py" entry --udp 127.0.0.1:$ENTRY --tunnel 127.0.0.1:$TUNNEL >/dev/null 2>&1 & pids+=($!)
sleep 1.5

fail=0
run() {  # run LABEL ARGS...
  local label="$1"; shift
  echo "=== $label"
  python3 "$here/udp-probe.py" client "$@" || fail=1
  echo
}
run "baseline: straight to the echo server (no bridge)" --host 127.0.0.1 --port $ECHO
run "through the bridge, steady traffic"               --host 127.0.0.1 --port $ENTRY
run "through the bridge, burst of mixed sizes"         --host 127.0.0.1 --port $ENTRY --interval 0 --count 120 --sizes 64,512,1200
echo "=== through the bridge, three players at once"
for i in 1 2 3; do
  python3 "$here/udp-probe.py" client --host 127.0.0.1 --port $ENTRY --count 150 > "/tmp/ct-selftest-$i.txt" & cp=$!
  cpids+=($cp)
done
for p in "${cpids[@]}"; do wait "$p" || fail=1; done
grep -h RESULT /tmp/ct-selftest-*.txt; rm -f /tmp/ct-selftest-*.txt
echo
if (( fail )); then echo "SELF-TEST FAILED"; exit 1; else echo "SELF-TEST PASSED"; fi

#!/usr/bin/env bash
# sync.sh - commit anything outstanding, rebase on GitHub's copy, and push.
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"
git add -A
git diff --cached --quiet || git commit -q -m "sync: $(date '+%F %H:%M')"
git pull --rebase --quiet
git push --quiet
msg="Synced $(basename "$root") with GitHub"
echo "$msg"
command -v notify-send >/dev/null && notify-send "CopperToolchain" "$msg" || true

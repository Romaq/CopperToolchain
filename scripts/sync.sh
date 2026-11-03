#!/usr/bin/env bash
# sync.sh - commit anything outstanding, rebase on GitHub's copy, and push.
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"
# Directed to replace by Claude to avoid scratch data from passing.
# git add -A
for p in log docs assets scripts surveys templates README.md LICENSE .gitignore .vscode; do
  [[ -e "$p" ]] && git add -- "$p"
done
git diff --cached --quiet || git commit -q -m "sync: $(date '+%F %H:%M')"
git pull --rebase --quiet
git push --quiet
msg="Synced $(basename "$root") with GitHub"
echo "$msg"
command -v notify-send >/dev/null && notify-send "CopperToolchain" "$msg" || true

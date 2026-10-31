#!/usr/bin/env bash
# setup-repo.sh - ONE-TIME: make this directory a git repo and push it to GitHub.
# Prerequisite: create the repo on GitHub first (no README or .gitignore). A license added at
# creation is fine: GitHub then holds an initial commit, which is rebased under before pushing.
# Usage: scripts/setup-repo.sh [remote-url]
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
remote="${1:-https://github.com/Romaq/CopperToolchain.git}"
cd "$root"

git config user.email >/dev/null || { echo "Set your identity first: git config --global user.name 'Name'; git config --global user.email 'you@example.com'" >&2; exit 1; }

mkdir -p log assets docs templates
for d in assets docs templates; do touch "$d/.gitkeep"; done

[[ -d .git ]] || git init -q -b main
git add -A
git diff --cached --quiet || git commit -q -m "Initial commit: scripts, conversation log, project layout"
git remote get-url origin >/dev/null 2>&1 || git remote add origin "$remote"
git branch -M main
if git ls-remote --exit-code --heads origin main >/dev/null 2>&1; then
  echo "GitHub already has commits on main (e.g. a LICENSE); rebasing onto them..."
  git pull --rebase origin main
fi
git push -u origin main
echo "Done. Repo: ${remote%.git}"

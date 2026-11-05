#!/usr/bin/env bash
# bootstrap-project.sh - create the local project folder and git repository for a new
# "Claude.ai project + GitHub repository" pair, with the logging, privacy, and survey tools in place.
#
# Usage:
#   ./bootstrap-project.sh "<Project Name>" <github-user> [--repo NAME] [--dir PATH] [--remote URL] [--no-hook]
#
#   <Project Name>  the name for BOTH the Claude.ai project and (in slug form) the repository
#   --repo NAME     repository name if you do not want the automatic slug (spaces removed, a leading "The " dropped)
#   --dir PATH      where to create the project (default: ~/Projects/<repo>)
#   --remote URL    push to this existing, empty GitHub repository when finished
#   --no-hook       do not install the pre-push privacy hook
#
# This script cannot create the Claude.ai project: that is done in the web interface (see START-HERE.md).
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
name="${1:-}"; user="${2:-}"; shift 2 2>/dev/null || true
repo=""; dir=""; remote=""; hook=1
while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)    repo="${2:?--repo needs a name}"; shift ;;
    --dir)     dir="${2:?--dir needs a path}"; shift ;;
    --remote)  remote="${2:?--remote needs a URL}"; shift ;;
    --no-hook) hook=0 ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
  shift
done
if [[ -z "$name" || -z "$user" ]]; then
  sed -n '2,15p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 2
fi

if [[ -z "$repo" ]]; then
  repo="$(printf '%s' "$name" | sed 's/^[Tt]he //' | tr -d '[:space:]' | tr -cd 'A-Za-z0-9._-')"
fi
[[ -n "$repo" && "$repo" =~ ^[A-Za-z0-9._-]+$ ]] || { echo "Repository name must use letters, digits, dots, hyphens, or underscores." >&2; exit 2; }
dir="${dir:-$HOME/Projects/$repo}"
if [[ -e "$dir" && -n "$(ls -A "$dir" 2>/dev/null)" ]]; then
  echo "Refusing to use $dir: it exists and is not empty." >&2; exit 1
fi
git config user.email >/dev/null 2>&1 || { echo "Set your git identity first: git config --global user.name 'Your Name'; git config --global user.email '<your-email>'" >&2; exit 1; }

echo "Project : $name"
echo "Repo    : $user/$repo"
echo "Folder  : $dir"

mkdir -p "$dir"
cp -a "$here/kit/." "$dir/"
mkdir -p "$dir/log"
touch "$dir/log/.gitkeep"

# Fill in the placeholders in the templates.
for f in "$dir/templates/claude-project-instructions.md"; do
  sed -i "s|{{PROJECT}}|$name|g; s|{{USER}}|$user|g; s|{{REPO}}|$repo|g" "$f"
done

printf 'surveys/responses/\ntmp/\n' > "$dir/.gitignore"

cat > "$dir/README.md" << MD
# $name

A project run with Claude: its creation, decisions, and progress are logged here.

- \`log/\`: dated conversation logs
- \`docs/\`: goals, decisions, and runbooks
- \`assets/\`: inventory of expertise and hardware
- \`scripts/\`: logging, syncing, and privacy-check tools
- \`surveys/\`: goals and skills surveys (answers stay private)
- \`prompts/\`: reusable prompts
- \`templates/\`: reusable templates, including the Claude project instructions

Chat name: $name. Repository: $repo.
MD

cd "$dir"
chmod +x scripts/*.sh
git init -q -b main
(( hook )) && bash scripts/install-hooks.sh
git add -A
git commit -q -m "Initial commit: project skeleton and tools"
bash scripts/privacy-check.sh --all || echo "(Review the findings above before the first push.)"

if [[ -n "$remote" ]]; then
  git remote add origin "$remote"
  if git ls-remote --exit-code --heads origin main >/dev/null 2>&1; then git pull --rebase origin main; fi
  git push -u origin main
  echo "Pushed to $remote"
fi

cat << NEXT

Done. Next steps:

 1. GitHub: $( [[ -n "$remote" ]] && echo "the repository is already pushed to $remote." || echo "create a repository named $repo under $user on github.com (New repository; no README or .gitignore; a license is optional),
    then, in $dir:
      git remote add origin https://github.com/$user/$repo.git
      git push -u origin main" )
 2. Claude.ai: create a project named "$name" and paste in the instructions from
    $dir/templates/claude-project-instructions.md (fill in the 'About this project' paragraph first).
 3. Read START-HERE.md for the rest of the order of work.
NEXT

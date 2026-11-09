# CopperToolchain tools available to customer projects

Source: https://github.com/Romaq/CopperToolchain (license: 0BSD)
Manifest date: 2026-11-09 (hand-written stopgap; a generated version will replace it)

A new project gets its scripts from the starter kit (`templates/new-project-kit/`), not from CopperToolchain's own `scripts/` folder.
Platform: the scripts were tested on Linux only. The macOS clipboard line is untested, and Windows is not covered.

## Scripts

| Tool | Where | Purpose | Notes for customers |
|---|---|---|---|
| `bootstrap-project.sh` | `templates/new-project-kit/` | Creates a project folder and git repo with the kit's tools, templates, prompts and surveys, installs the pre-push hook, runs a privacy check and makes the first commit | Usage: `./bootstrap-project.sh "<Name>" <github-user> [--repo NAME] [--dir PATH] [--remote URL] [--no-hook]`. The repo name is the project name with spaces removed and a leading "The " dropped; use `--repo` to override. Default folder is `~/Projects/<repo>`; it refuses a non-empty folder and needs your git identity set. It pushes only if you give `--remote`; omit it if you add a LICENSE on GitHub before the first push. It does not create the Claude.ai project, and it does not yet create `tools/FROM-COPPERTOOLCHAIN.md`. |
| `log-turn.sh` | `kit/scripts/` | Appends a conversation turn from the clipboard to the dated log and commits it | Linux only. Needs `xclip`, `xsel` or `wl-paste`. Commits every turn, and re-runs itself on the host inside a Flatpak sandbox. Speaker label via `CT_USER_LABEL`. `--turn` forces the number. The first turn of a day continues from the newest earlier log in the same repo, so a new project's first turn needs `--turn 1`. A failed commit is not reported (known issue). Notification title still says "CopperToolchain" (cosmetic). |
| `sync.sh` | `kit/scripts/` | Stages explicit paths, commits, rebases, pushes | Stages only: `log docs assets scripts surveys templates prompts README.md LICENSE .gitignore .vscode`. Anything else, such as a `tools/` folder or a root-level `STATE.md`, must be added to the list. Re-runs on the host inside a Flatpak. |
| `privacy-check.sh` | `kit/scripts/` | Scans what is about to be pushed for personal data and secrets | Patterns in `privacy-patterns.txt`. It cannot recognize names, health, money or family details. |
| `privacy-patterns.txt` | `kit/scripts/` | Pattern list used by the check | Data file; edit freely. |
| `privacy-allow.txt` | `kit/scripts/` | Exact-match exceptions for the check | Ships with three entries (`git@github.com`, `127.0.0.1`, `0.0.0.0`). Per repo; add your own. |
| `install-hooks.sh` | `kit/scripts/` | Installs the pre-push hook that runs the privacy check | Once per clone. Verified by TLC. |
| `setup-repo.sh` | CopperToolchain `scripts/` | CopperToolchain's own one-time setup: from the CopperToolchain root it runs `git add -A`, commits and pushes | **Do not copy.** Its only argument is a remote URL, which defaults to `Romaq/CopperToolchain`. It creates no project, copies no kit and installs no hook. Use `bootstrap-project.sh`. |
| `udp-bridge.py`, `udp-probe.py`, `udp-selftest.sh` | CopperToolchain `scripts/` | UDP game-hosting tunnel tools (UDP carried inside an SSH reverse tunnel) | Not needed by TLC and unverified from TLC's side. Self-test passes on one machine; a real SSH, relay and game test is still pending. |

## Other kit material

| Item | Where | Purpose |
|---|---|---|
| Starter guide | `templates/new-project-kit/START-HERE.md` | Order of work for a new project |
| Prompts 1 to 5 | `kit/prompts/` | Naming, goals from a survey, digest of the CopperToolchain logs, questions for CopperToolchain, choosing a logging method |
| Templates | `kit/templates/` | Claude project instructions and goals template |
| Surveys | `kit/surveys/` | Goals survey and the skills evaluation rubric (answers stay private) |
| Runbook | `kit/docs/runbooks/sensitive-data-in-git.md` | What to do when something sensitive is committed, in proportion to what leaked |
| Privacy check guide | `kit/docs/privacy-check.md` | When and how to run the privacy check |

Copied scripts are recorded in the customer repo's `tools/FROM-COPPERTOOLCHAIN.md` with the source link and commit.

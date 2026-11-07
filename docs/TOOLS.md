# CopperToolchain tools available to customer projects

Source: https://github.com/Romaq/CopperToolchain (license: 0BSD)
Manifest date: 2026-11-06 (hand-written stopgap; a generated version will replace it)

A new project gets its scripts from the starter kit, not from CopperToolchain's own `scripts/` folder.

| Tool | Where | Purpose | Notes for customers |
|---|---|---|---|
| `bootstrap-project.sh` | `templates/new-project-kit/` | Creates a project folder and git repo with the tools below installed, the pre-push hook, and a first commit | Usage: `./bootstrap-project.sh "<Name>" <github-user> [--repo NAME] [--dir PATH] [--remote URL] [--no-hook]`. Run it without `--remote` if you add a LICENSE file before the first push. |
| `log-turn.sh` | `kit/scripts/` | Appends a conversation turn from the clipboard to the dated log and commits it | Speaker label via `CT_USER_LABEL`. Notification title still says "CopperToolchain" (cosmetic). |
| `sync.sh` | `kit/scripts/` | Stages explicit paths, commits, rebases, pushes | New top-level folders must be added to its path list. |
| `privacy-check.sh` | `kit/scripts/` | Scans what is about to be pushed for personal data and secrets | Patterns in `privacy-patterns.txt`, exact-match exceptions in `privacy-allow.txt` (per repo). |
| `install-hooks.sh` | `kit/scripts/` | Installs the pre-push hook that runs the privacy check | Once per clone. |
| `setup-repo.sh` | CopperToolchain `scripts/` | CopperToolchain-specific first push | **Do not copy.** Default remote is hard-coded. Use `bootstrap-project.sh`. |
| `udp-bridge.py`, `udp-probe.py`, `udp-selftest.sh` | CopperToolchain `scripts/` | UDP game-hosting tunnel tools | Not needed by TLC. |

Copied scripts are recorded in the customer repo's `tools/FROM-COPPERTOOLCHAIN.md` with the source link and commit.

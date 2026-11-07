# Handoff state (2026-11-03)

Purpose: let a fresh Claude conversation in this project continue without re-reading the whole log.
Update it at the end of each session (ask Claude to rewrite it), commit it, and upload the new copy to the project's files.

## The project in one paragraph

CopperToolchain is a Claude.ai project paired with this GitHub repository. It documents its own creation, and it
builds scripts, processes, and plans for running other projects, starting with a home lab. Read `docs/PROJECT-GUIDE.md`
for the map of the repository and `docs/roadmap.md` and `docs/goals.md` for direction.

## Conventions to keep

- Replies start and end with `---` and begin with `## 🤖 CLAUDE · Turn N · date`. The user's turn number is authoritative: ask for it if unsure.
- The log is public. Flag personal details before doing anything else, offer placeholder wording, never repeat them in replies or files. Private files are attached, not pasted.
- Be direct and honest; say what was tested and what was not; keep steps small; apply the five-question test before adding any service.
- Inventory additions: give notice first, then supply the entry, and let the user apply it.
- Scripts run on the host through system keyboard shortcuts, because the editor is a sandboxed Flatpak.
- Claude cannot fetch GitHub file pages and its sandbox has no SSH or network: anything involving a real tunnel is untested until the user runs it.
- Work in one fresh conversation per task; end each session by rewriting this file.

## Decisions so far

1. Repository `CopperToolchain` is public; scripts live in `scripts/`; `sync.sh` stages explicit paths only.
2. A pre-push privacy check is installed; the allowlist requires exact matches. A stray-file incident was judged low sensitivity and accepted (`docs/decisions/`).
3. Notifications: Gotify on the home lab server, working with Proxmox's test message. Later: an outside heartbeat that alerts on silence, and UPS monitoring.
4. Keep it simple: no reverse proxy for now; trust the Proxmox certificate authority on the client first; be cautious with Webmin.
5. UDP for hosted games: an SSH reverse tunnel carrying a UDP-in-TCP bridge, verified with a probe that can fail; WireGuard is the fallback if play feels laggy.
6. The `LICENSE` for this project is 0BSD.

## Current work, in order

1. Apply Gotify to every service and machine that currently emails alerts; verify each and record it in a table (source, method, test, date, result). No tokens in the repository.
2. LAN test of the UDP tool using the game server container, a stand-in relay container, and the desktop client (steps in the logs: search `stand-in relay` and `Real game stage`). Hytale is installed on the desktop client and in the game-server container; Gotify already reaches the phone from Proxmox's test.
3. Onboarding a friend (DJV22) who will build a similar project for his own lab: the kit is in `templates/new-project-kit/`. Answer his question blocks (`QUESTION FOR THE COPPERTOOLCHAIN PROJECT`) when the user pastes them.
4. Survey 2 (skills evaluation): only when the user asks, in a fresh conversation, with the private answers attached.
5. Home lab sprint afterwards: notifications, then backups, updates, UPS monitoring, certificates.

## Small items pending

- Inventory candidates awaiting a yes: extra hardware entries, Client storage details, the study-habit entry.
- Add the three roadmap lines suggested after the notification design.

## Where to look

`docs/PROJECT-GUIDE.md` (map), `docs/runbooks/` (sensitive data in git, UDP over SSH), `docs/decisions/`, `assets/` (inventory), `surveys/` (templates), `templates/new-project-kit/` (the starter kit), `log/` (full history; search by phrase, not by turn number).

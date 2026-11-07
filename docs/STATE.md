# Handoff state (2026-11-07)

Purpose: let a fresh Claude conversation in this project continue without re-reading the whole log.
Update it at the end of each session (ask Claude to rewrite it), commit it, and upload the new copy to the project's files.

## The project in one paragraph

CopperToolchain is a Claude.ai project paired with this GitHub repository. It documents its own creation, and it
builds scripts, processes, and plans for running other projects, starting with a home lab. Read `docs/PROJECT-GUIDE.md`
for the map of the repository and `docs/roadmap.md` and `docs/goals.md` for direction.

## Conventions to keep

- Replies start and end with `---` and begin with `## 🤖 CLAUDE · Turn N · date`. The user's turn number is authoritative: ask for it if unsure.
- The log is public. Flag personal details before doing anything else, offer placeholder wording, never repeat them in replies or files. Private files are attached, not pasted.
- Be direct and honest; say what was tested and what was not; keep steps small; apply the five-question test (`docs/runbooks/can-vs-should.md`) before adding any service.
- Inventory additions: give notice first, then supply the entry, and let the user apply it.
- Scripts run on the host through system keyboard shortcuts, because the editor is a sandboxed Flatpak.
- Claude cannot fetch GitHub file pages and its sandbox has no SSH or network: anything involving a real tunnel is untested until the user runs it.
- Work in one fresh conversation per task; end each session by rewriting this file.
- Session titles: `<PROJECT> · YYYY-MM-DD · <task>`, the date being the day the session happens. Add "(day 2)" for a declared multi-day task.
- Every reply that ends a session, or produces something the other project needs, closes with a HANDOFF CHECK block (see below).

## Decisions so far

1. Repository `CopperToolchain` is public; scripts live in `scripts/`; `sync.sh` stages explicit paths only.
2. A pre-push privacy check is installed; the allowlist requires exact matches. A stray-file incident was judged low sensitivity and accepted (`docs/decisions/`).
3. Notifications: Gotify on the home lab server, working with Proxmox's test message. Later: an outside heartbeat that alerts on silence, and UPS monitoring.
4. Keep it simple: no reverse proxy for now; trust the Proxmox certificate authority on the client first; be cautious with Webmin.
5. UDP for hosted games: an SSH reverse tunnel carrying a UDP-in-TCP bridge, verified with a probe that can fail; WireGuard is the fallback if play feels laggy.
6. The `LICENSE` for this project is 0BSD (`docs/decisions/004-LICENSE.md`).
7. TLC (The Long Climb) is a separate Claude.ai project with its own repository, a customer of this project's tools. Modpack work stays in TLC; generic tooling is built here.
8. Cadence: alternate days between this project and TLC, one fresh conversation per task. Exceptions: a tool here is blocking TLC, or a declared multi-day task (note start and expected end below).

## Cross-project: The Long Climb (TLC)

- TLC credits CopperToolchain in its README. Copied scripts are recorded in `tools/FROM-COPPERTOOLCHAIN.md` in the TLC repo.
- TLC reads `docs/TOOLS.md`, `docs/PROJECT-GUIDE.md`, `docs/runbooks/can-vs-should.md` and `templates/new-project-kit/` through a GitHub source on its project (never `log/`). After committing a change to any of them, click Sync in TLC's project.
- `docs/TOOLS.md` is a hand-written stopgap until a generator exists. New projects get scripts from the kit (`bootstrap-project.sh`), not from `scripts/`. Do not copy `setup-repo.sh`: its default remote is hard-coded.
- TLC sends needs as `REQUEST FOR THE COPPERTOOLCHAIN PROJECT` blocks; record them in `docs/requests/`.
- TLC's earlier work (three planning docs, two scripts, two SVG logos, a handoff note for this project) is not yet exported from its old conversations.

HANDOFF CHECK block:

- Upload to [other project] files / Select or Sync in its GitHub source: [file, or "none"]
- Paste into [other project] chat: [block, or "none"]
- Commit in [other repo]: [file, or "none"]

## Current work, in order

1. TLC first session, planned Sunday 2026-11-08: `TLC · 2026-11-08 · Repo setup and prologue`. TLC creates its repository from the kit and logs the earlier context as Turn 1.
2. Monday 2026-11-09: `CT · 2026-11-09 · TOOLS.md generator`. Script-header convention, generated `docs/TOOLS.md`, `sync.sh` integration. Bring TLC's handoff note.
3. Apply Gotify to every service and machine that currently emails alerts; verify each and record it in a table (source, method, test, date, result). No tokens in the repository.
4. LAN test of the UDP tool using the game server container, a stand-in relay container, and the desktop client (search the logs for `stand-in relay` and `Real game stage`).
5. Onboarding a friend (DJV22): the kit is in `templates/new-project-kit/`. Answer his question blocks when the user pastes them.
6. Survey 2 (skills evaluation): only when the user asks, in a fresh conversation, with the private answers attached.
7. Home lab sprint afterwards: backups, updates, UPS monitoring, certificates.

## Small items pending

- Set the `docs/TOOLS.md` manifest date to 2026-11-07, commit, push, and confirm the `bootstrap-project.sh` row is there.
- Fix the spelling in `docs/runbooks/can-vs-should.md` ("Malcolm", "Jurassic").
- Record the TLC relationship and cadence in `docs/decisions/` as the next numbered entry.
- Inventory candidates awaiting a yes: extra hardware entries, Client storage details, the study-habit entry.
- Add the three roadmap lines suggested after the notification design.

## Where to look

`docs/PROJECT-GUIDE.md` (map), `docs/runbooks/`, `docs/decisions/`, `assets/` (inventory), `surveys/` (templates), `templates/new-project-kit/` (the starter kit), `log/` (full history; search by phrase, not by turn number).

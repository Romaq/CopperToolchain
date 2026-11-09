# Handoff state (2026-11-09)

Purpose: let a fresh Claude conversation in this project continue without re-reading the whole log.
Update it at the end of each session (ask Claude to rewrite it), commit it, and upload the new copy to the project's files.

## The project in one paragraph

CopperToolchain is a Claude.ai project paired with this GitHub repository. It documents its own creation, and it
builds scripts, processes, and plans for running other projects, starting with a home lab. Read `docs/PROJECT-GUIDE.md`
for the map of the repository and `docs/roadmap.md` and `docs/goals.md` for direction.

## Names (use these terms, and gently correct misuse)

- `short_name`: CT (this project), TLC (The Long Climb). Easy to type; may collide with outside names.
- `long_name`: "The Copper Toolchain". Least collision risk. Spaces allowed.
- `directory_name`: `CopperToolchain`. The long name made POSIX- and Windows-safe: only `A-Z a-z 0-9 . _ -`, no spaces, no `: < > " / \ | ? *`.
- In scripts use lowercase with underscores (`short_name`) or UPPER_CASE for exported values. Projects live under `~/Projects/` (plural).

## Conventions to keep

- Replies start and end with `---`. Headings are `## 🤖 CT CLAUDE · Turn N · date` (this project) and `## 🧑 CT USER · Turn N · date`. The emoticons are hard-coded in the scripts; the label carries the `short_name`. The user's turn number is authoritative: ask for it if unsure.
- Until the log-turn rewrite lands, the script still writes `🧑 USER`; the user edits by hand if wanted. Its turn-number pattern accepts any label.
- The log is public. Flag personal details before doing anything else, offer placeholder wording, never repeat them in replies or files. Private files are attached, not pasted. Never ask for a paste that would contain a name or email (for example raw `git log --show-signature`).
- Be direct and honest; say what was tested and what was not; keep steps small; apply the five-question test (`docs/runbooks/can-vs-should.md`) before adding any service.
- Design maxim: make mistakes hard to make, easy to catch, and easy to correct. Prefer simple, scripted automation over manual tracking.
- Inventory additions: give notice first, then supply the entry, and let the user apply it.
- Scripts run on the host through system keyboard shortcuts, because the editor is a sandboxed Flatpak.
- Claude sees only the synced snapshot of selected repo files (plus anything attached). It cannot see live `git status`, unpushed commits, signing setup or shortcuts, its sandbox has no SSH or network, and it cannot fetch GitHub file pages. Anything involving the live repo or a real tunnel is untested until the user runs it.
- One fresh conversation per task; end each session by rewriting this file.
- Session titles: `<short_name> · YYYY-MM-DD · <task>`. Two sessions on one day get `a` and `b` after the date (`2026-11-09a`). Add "(day 2)" for a declared multi-day task.
- Every reply that ends a session, or produces something the other project needs, closes with a HANDOFF CHECK block.
- Offer files as downloads to replace by hand-free copying where possible; the user prefers the method least prone to human error.

Session start checklist: (a) name the chat `<short_name> · date · topic`; (b) confirm which repo the shortcut will write to (the notification names it); (c) log the first turn.

HANDOFF CHECK block:

- Upload to [other project] files / Select or Sync in its GitHub source: [file, or "none"]
- Paste into [other project] chat: [block, or "none"]
- Commit in [other repo]: [file, or "none"]

## Decisions so far

1. Repository `CopperToolchain` is public; scripts live in `scripts/`; `sync.sh` stages explicit paths only.
2. A pre-push privacy check is installed; the allowlist requires exact matches. A stray-file incident was judged low sensitivity and accepted (`docs/decisions/`).
3. Notifications: Gotify on the home lab server, working with Proxmox's test message. Later: an outside heartbeat that alerts on silence, and UPS monitoring.
4. Keep it simple: no reverse proxy for now; trust the Proxmox certificate authority on the client first; be cautious with Webmin.
5. UDP for hosted games: an SSH reverse tunnel carrying a UDP-in-TCP bridge, verified with a probe that can fail; WireGuard is the fallback if play feels laggy.
6. The `LICENSE` is 0BSD (`docs/decisions/004-LICENSE.md`).
7. TLC (The Long Climb) is a separate Claude.ai project with its own repository, a customer of this project's tools. Modpack work stays in TLC; generic tooling is built here. `docs/TONE.md` belongs to TLC and has been moved there.
8. Cadence: alternate days between this project and TLC, one fresh conversation per task. Exceptions: a tool here is blocking TLC, or a declared multi-day task (note start and expected end below).
9. Per-project logging design (accepted, not yet built), below.

## Design: per-project logging (the current task)

Problem: shortcuts and `log-turn.sh` are tied to the CT root, so TLC turns were logged and committed in CT.

- **One shared file** `~/.config/copper/projects`: first line `active <short_name>`, then one `short_name<TAB>path` line per project. `SOS <short_name>` as the first clipboard line rewrites the `active` line; later presses log to the active project. Refuse an unregistered name.
- **`project.conf` in each repo** holds `short_name`, `long_name`, `directory_name`; the scripts read it. `bootstrap-project.sh` should fill it in from a third argument (parked).
- **Every notification names the project**: `Logged user turn 46 → CT`.
- **Closed or unclosed is derived from the log**, with no tracking folder: a session is closed if its last user turn starts with `COS <short_name>` and a Claude turn follows. At the next `SOS`, an unclosed previous log gets a warning block, and `log-turn.sh close --previous` appends a "closed late, reason unknown" note.
- **Numbering:** a new repo's first turn is 1, without forcing `--turn`. Heading labels use `short_name`.
- **Commit failure must be loud**: replace `|| true` after the commit with a notification and non-zero exit.
- **`sync.sh`** path list: add `tools` and any root `STATE.md`; take the list from one place.
- The script cannot rename the chat; the notification shows the suggested name.
- Not yet decided: the exact `SOS`/`COS` markers and the multi-day case.

## Cross-project: The Long Climb (TLC)

- TLC credits CopperToolchain in its README. Copied scripts are recorded in `tools/FROM-COPPERTOOLCHAIN.md` in the TLC repo.
- TLC reads `docs/TOOLS.md`, `docs/PROJECT-GUIDE.md`, `docs/runbooks/can-vs-should.md` and `templates/new-project-kit/` through a GitHub source on its project (never `log/`). After committing a change to any of them, click Sync in TLC's project.
- `docs/TOOLS.md` is a hand-written stopgap (manifest date 2026-11-09). New projects get scripts from the kit (`bootstrap-project.sh`), not from `scripts/`. Do not copy `setup-repo.sh`.
- TLC sends needs as `REQUEST FOR THE COPPERTOOLCHAIN PROJECT` blocks; record them in `docs/requests/`.
- The TLC repository exists and was created by `bootstrap-project.sh`. TLC's earlier work (three planning docs, two scripts, two SVG logos) may still need exporting from its old conversations.

## Current work, in order

1. **Session `CT · 2026-11-09b · log-turn rewrite`:** build the per-project logging design above (`log-turn.sh`, `sync.sh`), test what can be tested, and say what cannot.
2. Tuesday 2026-11-10: TLC resumes (`TLC · 2026-11-10 · ...`). If the rewrite runs over, TLC moves to Wednesday.
3. Then: Gotify on every service that emails (table of source, method, test, date, result; no tokens in the repo); LAN test of the UDP tool (search the logs for `stand-in relay` and `Real game stage`); onboarding a friend (DJV22) with the kit; Survey 2 only when asked; home lab sprint (backups, updates, UPS monitoring, certificates).

## Parked (do not raise unless asked or blocking)

- `bootstrap-project.sh` creating `tools/FROM-COPPERTOOLCHAIN.md`, `project.conf` and `{{SHORT_NAME}}`
- `docs/TOOLS.md` generator and its manifest columns
- GPG: TLC signing status, GitHub "Verified", a cold-cache test of the shortcut; the GPG discussion itself is held for the off-record process
- Off-record process (a separate chat that is never logged; only a sanitized summary returns)
- `privacy-check.sh --stdin` for checking a draft before sending
- `docs/runbooks/design-maxims.md` (collection file, one entry per maxim) with a pointer line in `can-vs-should.md`
- Stray-thoughts scratch file (outside the repo, one dated line each, triaged at session start)
- Hard-copy start and end card
- Tracked-items tool (two CSVs first, a database only if triggers appear)
- Windows path for friends (Cygwin to bootstrap; a Windows clone container in Proxmox later)
- Guidance on trust and self-hosted repositories for a customer
- Inventory candidates awaiting a yes (extra hardware entries, Client storage details, study-habit entry); the three roadmap lines; tidying `docs/decisions/005-mergeRequired.md` (stray `[`, unclosed code fence); heading of Turn 42 (`CLAUDE` to `CT CLAUDE`)

## Where to look

`docs/PROJECT-GUIDE.md` (map), `docs/runbooks/`, `docs/decisions/`, `assets/` (inventory), `surveys/` (templates), `templates/new-project-kit/` (the starter kit), `log/` (full history; search by phrase, not by turn number).

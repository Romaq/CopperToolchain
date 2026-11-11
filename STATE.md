# Handoff state (2026-11-11)

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

- Replies start and end with `---`. Headings are `## 🤖 CT CLAUDE · Turn N · date` (this project) and `## 🧑 CT USER · Turn N · date`. The emoticons are hard-coded in the scripts; the label carries the `short_name`. The user's turn number is authoritative. If the user's message does not state its number, ask in one line at the top of the reply instead of guessing (a guessed number put two replies out of step with the log on 2026-11-11).
- Until the log-turn rewrite lands, the script still writes `🧑 USER`; the user edits by hand if wanted. Its turn-number pattern accepts any label.
- The log is public. Flag personal details before doing anything else, offer placeholder wording, never repeat them in replies or files. Private files are attached, not pasted. Never ask for a paste that would contain a name or email (for example raw `git log --show-signature`).
- Be direct and honest; say what was tested and what was not; keep steps small; apply the five-question test (`docs/runbooks/can-vs-should.md`) before adding any service. The design maxims in `docs/runbooks/design-maxims.md` are the post-it phrases for snap judgements.
- Inventory additions: give notice first, then supply the entry, and let the user apply it.
- Scripts run on the host through system keyboard shortcuts, because the editor is a sandboxed Flatpak.
- Claude sees only the synced snapshot of selected repo files (plus anything attached). It cannot see live `git status`, unpushed commits, signing setup or shortcuts, its sandbox has no SSH or network, and it cannot fetch GitHub file pages. Anything involving the live repo or a real tunnel is untested until the user runs it.
- One fresh conversation per task; end each session by rewriting this file.
- Session titles: `<short_name> · YYYY-MM-DD · <task>`. Two sessions on one day get `a` and `b` after the date (`2026-11-09a`). Add "(day 2)" for a declared multi-day task. Both sessions still log to the same dated file, and the turn numbers continue.
- Mobile or chat-only moments (no scripts, no editor): use a chat inside this same project titled `CT · date · mobile capture`. It is capture-only: text to paste in later, logged by hand with `--turn N` at the desk. No separate project.
- Every reply that ends a session, or produces something the other project needs, closes with a HANDOFF CHECK block.
- Offer files as downloads to replace by hand-free copying where possible; the user prefers the method least prone to human error.
- Usage: Claude cannot see the meter or the reset time. The HANDOFF CHECK carries a rough light / moderate / heavy judgement from conversation size only; heavy means start a fresh conversation for the next task.

Session start checklist: (a) name the chat `<short_name> · date · topic`; (b) confirm which repo the shortcut will write to (the notification names it); (c) log the first turn; (d) state your turn number in the first message.

HANDOFF CHECK block:

- Upload to [other project] files / Select or Sync in its GitHub source: [file, or "none"]
- Paste into [other project] chat: [block, or "none"]
- Commit in [other repo]: [file, or "none"]
- Usage: [light / moderate / heavy], from conversation size only. I cannot see your meter or reset time, so check the usage page in Settings. [If heavy: start a fresh conversation for the next task.]

## Decisions so far

1. Repository `CopperToolchain` is public; scripts live in `scripts/`; `sync.sh` stages explicit paths only.
2. A pre-push privacy check is installed; the allowlist requires exact matches. A stray-file incident was judged low sensitivity and accepted (`docs/decisions/`).
3. Notifications: Gotify on the home lab server, working with Proxmox's test message. Later: an outside heartbeat that alerts on silence, and UPS monitoring.
4. Keep it simple: no reverse proxy for now; trust the Proxmox certificate authority on the client first; be cautious with Webmin.
5. UDP for hosted games: an SSH reverse tunnel carrying a UDP-in-TCP bridge, verified with a probe that can fail; WireGuard is the fallback if play feels laggy.
6. The `LICENSE` is 0BSD (`docs/decisions/004-LICENSE.md`).
7. TLC (The Long Climb) is a separate Claude.ai project with its own repository, a customer of this project's tools. Modpack work stays in TLC; generic tooling is built here. `docs/TONE.md` belongs to TLC and has been moved there.
8. Cadence: alternate days between this project and TLC, one fresh conversation per task. Exceptions: a tool here is blocking TLC, or a declared multi-day task (note start and expected end below).
9. Per-project logging design: accepted, build pending (decision 007, docs/decisions/007-liveLogging.md).
10. Design maxims live in `docs/runbooks/design-maxims.md` (own maxims, plus Schlock Mercenary maxims credited to Howard Tayler by number with a gloss). The five-question checklist stays separate in `can-vs-should.md`; rule 5 now reads "Is there an existing tool, or a simpler 80% solution?"

## Live logging: decided (007)

Build the minimal per-project logger first, with a two-session limit. Then run one timed Claude Code and SpecStory trial. Browser extensions and a CT split are not pursued now. See `docs/decisions/007-liveLogging.md`. If the two-session limit is passed, reopen the question.

## Design: per-project logging

Status: design accepted. The synced files do not show it built; confirm at session start by checking `scripts/log-turn.sh` for `SOS`.

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
- TLC is on hold until the live-logging decision is made. Next TLC day: to be set by the user.

## Current work, in order

1. **Next CT session:** build the minimal per-project logger (`log-turn.sh`, `sync.sh`). First confirm whether it is already built by checking `scripts/log-turn.sh` for `SOS`. Test what can be tested and say what cannot.
2. **After it works:** one timed Claude Code and SpecStory trial (cloud sync off, small CT task), then record the result in the decision's Actions.
3. TLC resumes (`TLC · date · ...`) once logging is settled.
4. Then: Gotify on every service that emails (table of source, method, test, date, result; no tokens in the repo); LAN test of the UDP tool (search the logs for `stand-in relay` and `Real game stage`); onboarding a friend (DJV22) with the kit; Survey 2 only when asked; home lab sprint (backups, updates, UPS monitoring, certificates).

## Parked (do not raise unless asked or blocking)

- `bootstrap-project.sh` creating `tools/FROM-COPPERTOOLCHAIN.md`, `project.conf` and `{{SHORT_NAME}}`
- `docs/TOOLS.md` generator and its manifest columns
- GPG: TLC signing status, GitHub "Verified", a cold-cache test of the shortcut; the GPG discussion itself is held for the off-record process
- Off-record process (a separate chat that is never logged; only a sanitized summary returns)
- `privacy-check.sh --stdin` for checking a draft before sending
- A "when it goes badly wrong" runbook page linked from Maxim 70, once a real incident gives it content
- Optional Schlock maxims 42, 52 and 53; user is checking exact quotes and numbers against the printed book
- Stray-thoughts scratch file (outside the repo, one dated line each, triaged at session start)
- Hard-copy start and end card
- Tracked-items tool (two CSVs first, a database only if triggers appear)
- Windows path for friends (Cygwin to bootstrap; a Windows clone container in Proxmox later)
- Guidance on trust and self-hosted repositories for a customer
- Inventory candidates awaiting a yes (extra hardware entries, Client storage details, study-habit entry); the three roadmap lines; tidying `docs/decisions/005-mergeRequired.md` (stray `[`, unclosed code fence); heading of Turn 42 (`CLAUDE` to `CT CLAUDE`)

## Where to look

`docs/PROJECT-GUIDE.md` (map), `docs/runbooks/` (including `design-maxims.md` and `can-vs-should.md`), `docs/decisions/`, `assets/` (inventory), `surveys/` (templates), `templates/new-project-kit/` (the starter kit), `templates/instructions/CT-project-instructions.md` (recovery copy of this project's instructions; edit the file first, then paste), `log/` (full history; search by phrase, not by turn number).

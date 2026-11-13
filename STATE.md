# Handoff state (2026-11-12, end of session)

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
- Live Logging (LL), identifier `liveLogging` (scripts: `live_logging`): committing the discussion stream into dated logs. See `docs/GLOSSARY.md`.
- Decision files are named `NNN-lowerCamelTopic.md`.
- HLE, Hound Lab Eval (`directory_name` `HoundLabEval`): the friend DJV22's parallel project, built from the kit. Separate project; CT does not manage it.

## Conventions to keep

- Replies start and end with `---`. Headings are `## 🤖 CT CLAUDE · Turn N · date` (this project) and `## 🧑 CT USER · Turn N · date`. The emoticons are hard-coded in the scripts; the label carries the `short_name`. The user's turn number is authoritative.
- Turn numbers: the user states the number in the first message of every conversation. Later messages may omit it if they continue the sequence; if a number cannot be inferred, ask in one line at the top of the reply instead of guessing (a guessed number put two replies out of step with the log on 2026-11-11).
- The live script writes `## 🧑 <short_name> USER · Turn N · date` and refuses a reply unless it is headed `## 🤖 <short_name> <AI> · Turn N · date`. Its turn-number pattern accepts any label.
- `SOS <short_name>` and `COS <short_name>` count only as the FIRST line of their own message. A bare `COS` is refused and not logged; a `COS` at the end of a longer message does not close the session. After `COS <short_name>`, log Claude's reply to finish closing.
- The log is public. Flag personal details before doing anything else, offer placeholder wording, never repeat them in replies or files. Private files are attached, not pasted. Never ask for a paste that would contain a name or email (for example raw `git log --show-signature`). Money matters (what can or cannot be afforded) are personal: use neutral wording such as "not available on the current plan".
- Be direct and honest; say what was tested and what was not; keep steps small; apply the five-question test (`docs/runbooks/can-vs-should.md`) before adding any service. The design maxims in `docs/runbooks/design-maxims.md` are the post-it phrases for snap judgements.
- Decision records are short; the detailed "why" lives in the log. Each decision has a `## Discussion` section pointing at a log file and a phrase to search for.
- Design maxim: make mistakes hard to make, easy to catch, and easy to correct. Prefer simple, scripted automation over manual tracking.
- Inventory additions: give notice first, then supply the entry, and let the user apply it.
- Scripts run on the host through system keyboard shortcuts, because the editor is a sandboxed Flatpak.
- Claude sees only the synced snapshot of selected repo files (plus anything attached). It cannot see live `git status`, unpushed commits, signing setup or shortcuts, its sandbox has no SSH or network, and it cannot fetch GitHub file pages. Anything involving the live repo or a real tunnel is untested until the user runs it.
- One fresh conversation per task; end each session by rewriting this file.
- Session titles: `<short_name> · YYYY-MM-DD · <task>`. Two sessions on one day get `a` and `b` after the date (`2026-11-09a`). Add "(day 2)" for a declared multi-day task. Both sessions still log to the same dated file, and the turn numbers continue.
- Mobile or chat-only moments (no scripts, no editor): use a chat inside this same project titled `CT · date · mobile capture`. It is capture-only: text to paste in later, logged by hand with `--turn N` at the desk. No separate project.
- Every reply that ends a session, or produces something the other project needs, closes with a HANDOFF CHECK block.
- Offer files as downloads rather than copy-paste blocks where possible; the user prefers the method least prone to human error. A patch needs the current file attached.
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
7. TLC (The Long Climb) is a separate Claude.ai project with its own repository, a customer of this project's tools (`docs/decisions/006-TLCRelationship.md`, being completed). Modpack work stays in TLC; generic tooling is built here. `docs/TONE.md` belongs to TLC and has been moved there.
8. Cadence: alternate days between this project and TLC, one fresh conversation per task. Exceptions: a tool here is blocking TLC, or a declared multi-day task (note start and expected end below).
9. Per-project logging: built (registry, `SOS`/`COS`, `project.conf`, hold, loud commit failure) and scratch-tested 2026-11-12; first real TLC run pending (decision 007, `docs/decisions/007-liveLogging.md`).
10. Design maxims live in `docs/runbooks/design-maxims.md` (own maxims, plus Schlock Mercenary maxims credited to Howard Tayler by number with a gloss). The five-question checklist stays separate in `can-vs-should.md`; rule 5 reads "Is there an existing tool, or a simpler 80% solution?"
11. Live Logging (007): build the minimal per-project logger first, within two sessions. Claude Code is not available on the current plan, so the SpecStory trial is dropped unless the CT project itself is at risk of failure. Browser exporter extensions and splitting CT into two projects are not pursued now.

## Live Logging: built (007)

The minimal per-project logger exists in the live `scripts/log-turn.sh` and `scripts/sync.sh`. Checked 2026-11-12 by reading both files and running them against scratch repos (registration, `SOS` switching, wrong-project and unregistered holds, reply-heading checks, `COS` closing, unclosed warning, `close --previous`, commit failure exit 3, explicit-path sync). Not tested by Claude: the real shortcuts, Flatpak re-run, clipboard, notifications, GPG signing from a shortcut.

How it works: `~/.config/copper/projects` (line 1 `active <short_name>`, then `short_name<TAB>path`), `project.conf` in each repo, every notification names the project, a new repo's first turn is 1, a failed commit is loud, `sync.sh` takes its path list from one place (`SYNC_PATHS`). Commands: `log-turn.sh status | register <name> <path> | close --previous [--yes]`.

Still undecided: the multi-day case (each new day's `SOS` warns about a continuing task's previous log), and whether a bare `COS` should mean an implied close (currently refused). The script cannot rename the chat; the notification shows the suggested name.

## Cross-project: The Long Climb (TLC)

- TLC credits CopperToolchain in its README. Copied scripts are recorded in `tools/FROM-COPPERTOOLCHAIN.md` in the TLC repo.
- TLC reads `docs/TOOLS.md`, `docs/PROJECT-GUIDE.md`, `docs/runbooks/can-vs-should.md` and `templates/new-project-kit/` through a GitHub source on its project (never `log/`). After committing a change to any of them, click Sync in TLC's project.
- `docs/TOOLS.md` is a hand-written stopgap (manifest date 2026-11-09). New projects get scripts from the kit (`bootstrap-project.sh`), not from `scripts/`. Do not copy `setup-repo.sh`.
- TLC sends needs as `REQUEST FOR THE COPPERTOOLCHAIN PROJECT` blocks; record them in `docs/requests/`.
- The TLC repository exists and was created by `bootstrap-project.sh`. TLC's earlier work (three planning docs, two scripts, two SVG logos) may still need exporting from its old conversations.
- TLC may use ChatGPT to design and implement a mod for the modpack. The workflow is not yet recorded (open questions in decision 006).
- TLC is on hold until Live Logging works. Next TLC day: to be set by the user.

## Current work, in order

Next session title: `CT · 2026-11-13 · Live Logging kit update (day 3)`. First message states the turn number. Declared multi-day task: Live Logging, start 2026-11-11, expected end 2026-11-13. The user will report the TLC test result at the start.

1. **Small items first (user at the desk):** commit `docs/decisions/007-liveLogging.md` (updated), `docs/GLOSSARY.md` and this STATE.md; run `scripts/log-turn.sh close --previous` for the unclosed log from 2026-11-11 if not already done.
2. **TLC test report:** a shortcut press while working on TLC writes to and commits in the TLC repo, its first turn is 1, and notifications name TLC. If that passes, TLC resumes.
3. **Kit update for DJV22 (issue #1 on the CT repository):** bring `templates/new-project-kit/` in line with the live logger: generic `log-turn.sh` and `sync.sh`, `project.conf` created and the project registered by `bootstrap-project.sh` (it currently creates neither), a close-out section in `START-HERE.md`. Attach the current `START-HERE.md` and the kit's `scripts/` folder. Optional: `scripts/live_logging-selftest.sh`, a re-runnable form of the 2026-11-12 scratch tests. Meanwhile DJV22 uses a manual close-out checklist; reply to issue #1 once it exists. No deadline for him: he asked for no rushing.
4. **Finish decision 006.** Four questions are open: (1) ChatGPT's role (design, code, or both; what it sees), (2) how its transcripts are logged and who reviews generated code, (3) the licence for the mod and the code, (4) whether the TLC README Tools section and `tools/FROM-COPPERTOOLCHAIN.md` exist.
5. Then: Gotify on every service that emails (table of source, method, test, date, result; no tokens in the repo); LAN test of the UDP tool (search the logs for `stand-in relay` and `Real game stage`); onboarding a friend (DJV22, HLE) with the updated kit; Survey 2 only when asked; home lab sprint (backups, updates, UPS monitoring, certificates).

## Parked (do not raise unless asked or blocking)

- Claude Code with SpecStory trial (revisit only if the CT project is at risk of failure or the plan changes)
- Bare `COS` as an implied close; detecting `COS` as the last line of a message; the multi-day warning noise
- HLE's repository as Context in this project (only once there is something to read)
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

`docs/PROJECT-GUIDE.md` (map), `docs/GLOSSARY.md`, `docs/runbooks/` (including `design-maxims.md` and `can-vs-should.md`), `docs/decisions/`, `assets/` (inventory), `surveys/` (templates), `templates/new-project-kit/` (the starter kit), `templates/instructions/CT-project-instructions.md` (recovery copy of this project's instructions; edit the file first, then paste), `log/` (full history; search by phrase, not by turn number).

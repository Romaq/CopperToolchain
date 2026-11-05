# CopperToolchain project guide

Read this first. It explains what the project is, lists its important elements, and says how to find
the surrounding discussion in the logs. Written 2026-11-03; the project keeps changing, so check the dates.

## What this project is

CopperToolchain is a Claude.ai project paired with this GitHub repository. Its short-term goal is to
document its own creation and progress, so that the repository is a faithful record of the work. Its
long-term goal is to produce scripts, processes, and plans that help run other projects, starting with
a home lab. The method is deliberately simple: work with Claude in a chat, copy each message into a dated
log with a script, check for personal details before anything is published, and write decisions down.

## How a log entry looks

Every message is a block that starts with a heading:

- `## 🧑 USER · Turn N · date` followed by the message as a quotation
- `## 🤖 CLAUDE · Turn N · date` followed by the reply, with horizontal rules around it

`log/log.md` holds the first conversation (hand-edited, early turns). Later sessions are in dated files
`log/YYYY-MM-DD.md`. Turn numbers can be off by one in places because early entries were edited by hand, so
**search for a phrase rather than a number**. For example: `grep -n "alert on silence" log/*.md`

## Important elements

| Element | What it is | Where it lives | Search the logs for |
|---|---|---|---|
| The founding plan | Purpose, the two phases (inventory, then self-documentation) | `log/log.md`, first turns | `Phase 1: Asset inventory` |
| Log format | Headings, rules, and numbering that make replies paste cleanly | project instructions, `templates/` | `Conversation log format` |
| Logging scripts | Copy a message, press a shortcut, and a script appends it to a dated log and commits | `scripts/log-turn.sh`, `scripts/sync.sh` | `log-turn.sh` |
| A sandbox surprise | An app packaged in a sandbox could not see a host tool, so shortcuts moved outside the app | the scripts, the logs | `Flatpak` |
| Privacy caution | Instruction block telling Claude to flag personal details before they are logged | project instructions | `Public-log privacy caution` |
| Privacy check and hook | Scans what is about to be pushed for addresses, keys, paths, and more; blocks the push | `scripts/privacy-check.sh`, `docs/privacy-check.md` | `privacy-check.sh` |
| A leak, handled in proportion | A scratch file was committed; triage by severity, then a decision to accept | `docs/runbooks/sensitive-data-in-git.md`, `docs/decisions/` | `git rm` and `proportion` |
| Asset inventory | Expertise and hardware as YAML, with a history for skill growth | `assets/` | `Inventory candidate` |
| Surveys | A goals survey, then a skills survey, answered privately and evaluated against written level definitions | `surveys/` | `Survey 1` and `Survey 2` |
| Goals and roadmap | Goals as workstreams, with "done looks like" lines, and a prioritized roadmap | `docs/goals.md`, `docs/roadmap.md` | `workstream` |
| UDP through an SSH tunnel | A bridge, a verifier that can fail, and a self-test | `scripts/udp-*`, `docs/runbooks/udp-over-ssh.md` | `udp-selftest` and `naive bridge` |
| Resilient notifications | A notifier that dies with the thing it watches needs an outside check | the logs | `alert on silence` |
| Keeping it simple | Five questions every new service must answer before it is added | the logs | `drawing the line` |
| Testing a stand-in | Using a spare container as a pretend relay to test for real | the logs | `stand-in relay` |

## Lessons learned (short)

- Say what was tested and what was not. A check that cannot fail proves nothing, so test it against a deliberately broken case.
- `git rm` removes a file from the newest snapshot only. History keeps it. Decide what to do in proportion to what leaked.
- Match the effort to the problem. A service that is hard to maintain is a cost, not a feature.
- Keep private answers out of the log: attach files instead of pasting, and use placeholders such as `[PRIVATE-1]` in replies.
- Stage explicit paths when syncing. `git add -A` is how scratch files get in.
- Matching a "harmless" value by substring lets lookalikes through; require an exact match.

## What is specific to this project (do not copy blindly)

The hardware, the network arrangement and its limits, the names, the file paths, the particular games and
services, and the personal goals. The pattern (log, check, decide, record) transfers; the details do not.

## Asking for more

Questions about the logs or the decisions behind them can be sent as a block in the format in
`templates/new-project-kit/kit/prompts/04-questions-for-copper-toolchain.md`. Basic questions are welcome.

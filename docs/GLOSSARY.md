# Glossary

Terms used across CopperToolchain (CT), The Long Climb (TLC) and Hound Lab Eval (HLE).
Rebuilt 2026-11-12 from `STATE.md` and the logs. Add a term when it is used twice without explanation.

## Projects

| Term | Meaning |
|---|---|
| **CT**, CopperToolchain, The Copper Toolchain | This project: a Claude.ai project paired with the `CopperToolchain` repository. It documents its own creation and builds scripts, processes and plans for other projects. All four spellings are synonyms. |
| **TLC**, The Long Climb | A separate Claude.ai project and repository for a Minecraft modpack. A customer of CT's tools. |
| **HLE**, Hound Lab Eval, HoundLabEval | A friend's parallel project, built from CT's starter kit for his own home lab. `short_name` HLE, `long_name` "Hound Lab Eval", `directory_name` `HoundLabEval`. Separate project and repository; CT does not manage it. |
| **DJV22** | The GitHub handle of the friend who runs HLE. |
| **Customer project** | Any project (TLC, HLE) that uses CT's tools. It asks for tools with a request block. |

## Names

| Term | Meaning |
|---|---|
| `short_name` | Easy-to-type project label: CT, TLC, HLE. |
| `long_name` | Full name, spaces allowed: "The Copper Toolchain". |
| `directory_name` | The long name made safe for folders and repositories: only `A-Z a-z 0-9 . _ -`. Example: `CopperToolchain`. |
| `project.conf` | Planned file in each repository holding the three names above. |

## Logging

| Term | Meaning |
|---|---|
| **Live Logging (LL)**, `liveLogging`, `live_logging` | Committing the discussion stream into dated logs as it happens. `liveLogging` is the identifier in prose and filenames; `live_logging` in scripts. |
| **Turn** | One message. Turn numbers continue across sessions on the same day and across days. The user's number is authoritative. |
| **Session** | One fresh conversation for one task. Titled `<short_name> · YYYY-MM-DD · <task>`; `a` and `b` after the date for two on one day; "(day 2)" for a declared multi-day task. |
| **SOS** `<short_name>` | Session-start marker: the first clipboard line when starting a session. In the design, it sets the active project. Until the script supports it, it is a typed marker only. |
| **COS** `<short_name>` | Close-of-session marker. A session counts as closed when its last user turn starts with COS and a Claude reply follows. |
| **Unclosed session** | A previous log with no COS. The design adds a warning at the next SOS and a "closed late, reason unknown" note. |
| `log-turn.sh` | Clipboard-to-log script. Appends a turn to the dated log and commits it. |
| `sync.sh` | Stages explicit paths, commits, rebases and pushes. |

## Process

| Term | Meaning |
|---|---|
| **HANDOFF CHECK** | Block closing a session-ending reply: what to upload, paste or commit in the other project, plus a rough usage judgement. |
| **REQUEST FOR THE COPPERTOOLCHAIN PROJECT** | Block a customer project sends when it needs a tool CT does not list. |
| **QUESTION FOR THE COPPERTOOLCHAIN PROJECT** | Block a customer project sends when its Claude cannot answer a question from CT's files. May be posted as a GitHub Issue. |
| **Manifest** | `docs/TOOLS.md`: the list of tools CT offers, with a manifest date. Hand-written for now. |
| **Kit** | `templates/new-project-kit/`: the starter kit a new project is created from. |
| **Decision record** | Short file in `docs/decisions/`, named `NNN-lowerCamelTopic.md`, with a `## Discussion` section pointing at a log file and a phrase to search for. |
| **Design maxims** | Short post-it rules for snap judgements, in `docs/runbooks/design-maxims.md`. |
| **Five questions** | The checklist in `docs/runbooks/can-vs-should.md`, applied before adding any service. |
| **Parked** | Deliberately postponed. Not raised unless asked or blocking. |
| **Stopgap** | A hand-written stand-in for something that will later be generated. |

## Home lab

| Term | Meaning |
|---|---|
| **Client** | The primary Linux workstation. |
| **Headless** | The Proxmox home-lab server. |
| **LAN** | The home network. |
| **Relay** | A host players can reach, running the UDP bridge's entry end. |
| **Stand-in relay** | A spare container on the LAN used as a pretend relay for testing. |

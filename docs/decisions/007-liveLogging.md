# 007: How to do live logging across projects

- Date: 2026-11-11
- Status: accepted
- Updated: 2026-11-12
- Term: Live Logging (LL), identifier `liveLogging`; see `docs/GLOSSARY.md`

## What happened
Logging shortcuts and `log-turn.sh` are tied to the CT repository root, so TLC turns were logged and committed in CT. A one-round search found no existing tool that covers per-project routing, session open and close, continued numbering, a loud commit failure, and the privacy check before push.

## Classification
Low sensitivity, per `docs/runbooks/sensitive-data-in-git.md`. The risk is a log committed to the wrong repository, which the privacy hook limits but does not prevent.

## Decision
Finish the minimal per-project logger in at most two sessions, as designed in STATE.md: a shared project list with `SOS <short_name>` selecting the active project, `project.conf` in each repo, notifications that name the project, a new repo's first turn numbered 1, and a commit failure that is loud instead of silent.

Everything else is parked: `bootstrap-project.sh` changes, the kit update, and the multi-day case.

Not chosen now:
- Browser exporter extensions. They read the whole page and solve neither routing nor numbering.
- Claude Code with SpecStory. It is not available on the current plan, so the trial is dropped unless the CT project itself is at risk of failure. It was never a replacement for the logger.
- Splitting CT into two projects. This fails question 5 of `can-vs-should.md` for now.

Maxims applied: "Make it work, then worry about making it work better" and "Reinventing the wheel is generally a bad plan unless you make a very nice wheel". Here the wheel was searched for and nothing fitted.

Until the logger is built, the interim safety is to check the notification for the repo name, and to move any misfiled log at close of day.

## Update 2026-11-12
The live `scripts/log-turn.sh` and `scripts/sync.sh` already contain the logger: a registry, `SOS` and `COS`, `project.conf` checks, a hold file, a loud commit failure, per-repo numbering and `close --previous`. Claude's scratch-repo tests passed; the real shortcut test showed the project name in the notification and the unclosed-session warning. Learned in use:
- `SOS` and `COS` count only as the FIRST line of their own message. A `COS CT` at the end of a longer message does not close the session.
- A bare `COS` (no name) is refused loudly and not logged, so that session shows as unclosed at the next `SOS`. The name is the check that you know which project you are closing.
- Parked alternative: accept a bare `COS` as an implied close of the active project, with the notification naming it. Revisit only if bare `COS` keeps happening.
- A session carried over several days has no `COS` until its last day, so each new day's `SOS` warns. The multi-day case is still undecided.

## Actions
- [x] Searched for existing tools (one round; nothing tested).
- [x] Build the minimal per-project logger (present in the live scripts).
- [x] Scratch-repo tests (Claude) and the first real `status` and `SOS CT` run (user).
- [ ] Real run on TLC: a shortcut press lands in the TLC repo, and its first turn is 1.
- [ ] Close yesterday's unclosed log with `log-turn.sh close --previous`.
- [x] Claude Code and SpecStory trial dropped (not available on the current plan).
- [x] Update STATE.md to record this decision.

## Discussion
- Design and the decision: `log/2026-11-11.md`, search for `Live Logging`. (Confirm the phrase when you commit.)
- Build check and tests: `log/2026-11-12.md`, search for `no patch is needed`.

## Revisit if
Misrouting still happens with the logger in place, or CT itself is at risk of failure (then reconsider Claude Code and the split). Also revisit the bare `COS` and multi-day rules if they keep causing warnings.

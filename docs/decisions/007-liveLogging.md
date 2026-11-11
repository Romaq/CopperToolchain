# 007: How to do live logging across projects

- Date: 2026-11-11
- Status: accepted

## What happened
Logging shortcuts and `log-turn.sh` are tied to the CT repository root, so TLC turns were logged and committed in CT. A one-round search found no existing tool that covers per-project routing, session open and close, continued numbering, a loud commit failure, and the privacy check before push.

## Classification
Low sensitivity, per `docs/runbooks/sensitive-data-in-git.md`. The risk is a log committed to the wrong repository, which the privacy hook limits but does not prevent.

## Decision
Finish the minimal per-project logger in at most two sessions, as designed in STATE.md: a shared project list with `SOS <short_name>` selecting the active project, `project.conf` in each repo, notifications that name the project, a new repo's first turn numbered 1, and a commit failure that is loud instead of silent.

Everything else is parked: the `COS` close check, `bootstrap-project.sh` changes, and the multi-day case.

Not chosen now:
- Browser exporter extensions. They read the whole page and solve neither routing nor numbering.
- Claude Code with SpecStory. Run one timed trial after the logger works, with cloud sync off, on a small CT task. It is not a replacement for step 1.
- Splitting CT into two projects. This fails question 5 of `can-vs-should.md` for now.

Maxims applied: "Make it work, then worry about making it work better" and "Reinventing the wheel is generally a bad plan unless you make a very nice wheel". Here the wheel was searched for and nothing fitted.

Until the logger is built, the interim safety is to check the notification for the repo name, and to move any misfiled log at close of day.

## Actions
- [x] Searched for existing tools (one round; nothing tested).
- [ ] Build and test the minimal per-project logger (two-session limit).
- [ ] One timed Claude Code and SpecStory trial after the logger works.
- [ ] Update STATE.md to record this decision.

## Revisit if
The logger takes more than two sessions, or it works but misrouting still happens, or the trial shows Claude Code is the better daily home for CT work. In any of those cases, reconsider the split too.

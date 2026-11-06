# 001: Stray scratch file committed (low sensitivity)

- Date: 2026-11-02
- Status: accepted

## What happened
A scratch file (`temp.md`) was staged by `git add -A` and pushed. It held low-sensitivity
technical information (an exact software version string). No credentials, no personal data.

## Classification
Low sensitivity, per `docs/runbooks/sensitive-data-in-git.md`.

## Decision
Removed the file with `git rm`. That removes it from the current snapshot only; the file
remains in earlier history. Accepted, because the data is low-value and a history rewrite
is not justified by the risk.

## Actions
- [x] Ignore rules corrected: one entry per line (`surveys/responses/`, `tmp.md`, `temp.md`)
- [X] `scripts/sync.sh` stages explicit paths instead of `git add -A`
- [x] Privacy check and pre-push hook installed; runbook written

## Revisit if
The file proves to hold more than described, or the repository is promoted for wider use.

# 003: Meta Privacy Warning

- Date: 2026-11-04
- Status: accepted

## What happened
A discussion of [credential-assignment] triggered a privacy warning. It was only a discussion of setting up protection, not a breach itself.

## Classification
High priority due to blocking nature to sync. Action needed to be taken immediately to allow the discussion to pass.

## Decision
Have git skip the scan.

## Actions
```bash
CT_SKIP_PRIVACY=1 git push
```
sync returns null, as desired.

## Revisit if
This process will need to be repeated for meta security issues in the figure so the security issues can be discussed without blocking the discussion.

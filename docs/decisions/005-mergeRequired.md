# 005: Merge required (Surprise!)

- Date: [2026-11-05
- Status: understood, no further action required.

## What happened
A surprise "branch merge" was required. This happened when I used Github to create a LICENSE through the webesite and committed it. This caused a situation requiring a merge between the two "branches."

## Classification
Low

## Decision
I was surprised, but understood what occured on reflection.

## Actions
- [X] The branches are merged and in sync using the following:
```bash
git config pull.rebase false
git pull
Merge made by the 'ort' strategy.
 LICENSE | 13 +++++++++++++
 1 file changed, 13 insertions(+)
 create mode 100644 LICENSE

## Revisit if
I should have pulled before resuming activity, if necessary closing out the existing work in the local repository.

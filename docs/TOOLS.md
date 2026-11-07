# CopperToolchain tools available to customer projects

Source: https://github.com/Romaq/CopperToolchain (license: 0BSD)
Manifest date: 2026-11-06 (hand-written stopgap; a generated version will replace it)
† = purpose inferred from the file name, not yet verified against the script.

| Script | Purpose | Customer notes |
|---|---|---|
| `log-turn.sh` | Appends conversation turns to the repo log | Used by TLC |
| `sync.sh` | Stages explicit paths, commits and pushes | Path list is specific to CopperToolchain; TLC must edit it to its own folders |
| `privacy-check.sh` | Scans for sensitive data before a push | Used by TLC |
| `privacy-patterns.txt` | Patterns that `privacy-check.sh` flags | Data file; TLC may extend it |
| `privacy-allow.txt` | Exact-match exceptions for the check | Per repo; TLC starts with its own empty list |
| `install-hooks.sh` | † Installs the git pre-push hook that runs the privacy check | Used by TLC |
| `setup-repo.sh` | Sets up a new project repository | Used by TLC; confirm usage before running |
| `udp-bridge.py` | UDP-in-TCP bridge for reverse-tunnel game hosting | Not needed by TLC |
| `udp-probe.py` | Probe that verifies the UDP tunnel and can fail | Not needed by TLC |
| `udp-selftest.sh` | LAN self-test for the UDP tool | Not needed by TLC |

Copying rule: a copied script is recorded in the customer repo's `tools/FROM-COPPERTOOLCHAIN.md`
with its source link and the commit it came from.

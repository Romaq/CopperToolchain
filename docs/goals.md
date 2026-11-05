# Goals (draft v1, 2026-11-03)

Restated from Survey 1 as five workstreams plus shared foundations. This version is safe to
publish: personal circumstances appear only as `[PRIVATE-n]` and are kept in private notes,
never in this repository. Priorities are the original ones; open questions are in the follow-up survey.

## Principles

- Every project stays something to look forward to: small steps, visible results, time-boxed sessions.
- Finish and document small pieces before taking on large ones.
- Backups come before anything that holds irreplaceable data.
- Anything shared publicly is checked first (`scripts/privacy-check.sh`).

## Workstreams

### A. The Long Climb: create and release a Minecraft modpack
- **Statement:** Build a modpack for play among friends and family, and release it publicly.
- **Why:** Gratitude and shared enjoyment for the people who play, and a contribution back to the Minecraft community.
- **Horizon:** 12 months
- **Done looks like:** The modpack is publicly released on CurseForge in a release-ready state, and the tools used to maintain it are public on GitHub.
- **So far:** An earlier attempt was set aside. The work now continues as its own project, with this toolchain supplying the process and tooling.
- **Depends on:** C only for UDP-based games; Minecraft Java Edition and perhaps others only requires TCP.
- **Priority:** 1

### B. Home lab foundations
- **Statement:** Put the home lab into dependable working order and make better use of the hardware already owned.
- **Why:** Stability and peace of mind, a base for building IT tools, and enjoyable use of idle assets.
- **Horizon:** 3 years, with ongoing growth.
- **Done looks like:** Regular scheduled backups with tested restores; notifications for tasks and failures; timely updates; devices that relied on a commercial home-automation service work without it.
- **So far:** Hardware is inventoried (`assets/hardware.yaml`); virtualization is in use; several earlier efforts were left unfinished.
- **Next:** Break this broad goal into small, separately finishable projects (see `docs/roadmap.md`).
- **Priority:** 2

### C. Secure game hosting for friends and family
- **Statement:** Host multiplayer games from the home network so invited friends and family can join securely, even though the network does not allow inbound connections.
- **Why:** Rich self-hosted games at no hosting cost, shared with people who cannot otherwise join.
- **Horizon:** 3 months
- **Done looks like:** A specific game (Hytale) is hosted at home and joined securely by invited players.
- **So far:** A TCP-only approach works for some traffic. Most modern games use UDP, which is not yet solved.
- **Open:** The approach is not yet chosen (see follow-up questions). This is the largest known skill gap.
- **Enables:** hosting Hytale and any other UDP-based games in A.
- **Priority:** 3

### D. Household library: organize, share, and safeguard
- **Statement:** One organized, de-duplicated collection of photos, music, video, and documents, reachable from every household device, with the right level of privacy for each kind.
- **Why:** Old photos tagged so they can be found and shared, music enjoyed without a subscription workaround, and records easy to find without re-scanning. `[PRIVATE-1]` covers records that need special handling.
- **Horizon:** 12 months
- **Done looks like:** No duplicates; everything reachable from shared or private storage as appropriate; a simple routine for adding new files and sharing the right ones.
- **So far:** A photo manager and a music tagger were tried and set aside when the volume felt too large. A password manager is available but not yet used for this.
- **Approach:** A short weekly session starting with one folder.
- **Depends on:** B (storage and backups).
- **Priority:** 4, deliberately kept below the projects that are most enjoyable.

### E. Professional presence (the "shingle")
- **Statement:** Build a stable professional presence (website, GitHub profile, and other channels) showing what I can do and that I am available for part-time, work-from-home IT work or teaching.
- **Why:** To develop and present IT skills that could earn modest income, and to practice working a regular day. `[PRIVATE-2]` covers circumstances that shape which arrangements are possible.
- **Horizon:** 12 months
- **Done looks like:** A stable site and profile, a plan to promote them, and a way to follow up on enquiries and raise rates over time.
- **Draws on:** The public work from A, B, and C as evidence.
- **Priority:** 5

## How the original goals map to these workstreams

| Original goal | Now |
|---|---|
| 1. The Long Climb | A |
| 2. Local IT toolset | B, plus the media-access part moved to D, plus the revenue idea moved to E |
| 3. Beating CGNAT | C |
| 4. Organizing memories | D |
| 5. My "shingle" | E |

## Overlaps resolved

- Hosting (C) serves both the modpack (A) and the single-game goal, so it is its own workstream.
- Storage and backups (B) underpin the library (D), so D depends on B.
- The revenue idea in the old goal 2 belongs with the professional presence (E).
- The public artifacts from A, B, and C are the evidence E needs.

## Shared foundations

- **Documentation habit:** every session logged (`log/`), decisions recorded (`docs/decisions/`).
- **Privacy hygiene:** the pre-push check and the runbook in `docs/runbooks/`.
- **Skill growth:** surveys and the `history` lines in `assets/expertise.yaml`.
- **Project management practice:** definition of done, next step, and blocker for each workstream.

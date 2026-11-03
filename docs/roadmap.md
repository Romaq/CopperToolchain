# Roadmap (draft)

Status: draft v0, 2026-11-02. A starting point to edit as priorities are clarified,
completed, and expanded. Update the date and keep finished items (mark them `[x]`) so the
record of progress stays intact. Detailed reasoning goes in `docs/decisions/`, not here.

Keep this file at the level of goals and outcomes. Hostnames, addresses, remote-access
arrangements, and other network details stay out of this public repository.

## Principles

- The project documents its own creation: every session is logged under `log/`.
- Anything reusable gets promoted to `templates/` with a standard header (purpose, inputs, requirements).
- Nothing counts as done until it has been tested, including restoring from backups.
- Check for personal details before pushing (`scripts/privacy-check.sh`).

## Now: core systems in working order

- [ ] **Inventory complete and committed** (`assets/hardware.yaml`, `assets/expertise.yaml`).
  Done when: both files are in the repo and every host and device in scope is listed.
- [ ] **Client and Headless in working order.** Done when: "working order" is defined in a
  short checklist (updates applied, services healthy, storage healthy) and both pass it. *(Define the checklist first.)*
- [ ] **Phone notifications** from Headless and Client (Gotify is the leading candidate).
  Done when: one real alert from each machine reaches the phone, and failures of the
  notifier itself are noticed.

## Next: protection

- [ ] **LAN backup plan for all hosts.** Scope: Client, Headless and its containers and VM,
  other laptops, phones. Done when: a written plan covers what is backed up, how often, where
  copies live, and how the offline drive is rotated, and **one restore has been tested per class of host**.
- [ ] **Timely security updates.** Done when: a routine exists for checking, applying, and
  confirming updates on every host, with a notification when something is overdue.

## Later: new capabilities

- [ ] **Home automation migration.** Configure the unused Home Assistant VM to replace the
  current cloud-based service. Done when: the existing household use cases work without the old service.
- [ ] **Tools for restricted inbound connectivity** (working title: Tools for CGNAT): carrying
  both TCP and UDP traffic over an SSH connection. Done when: a reusable, documented script
  supports both protocols and is tested.
- [ ] **Extend tooling to the other assets**, including converting the Windows laptop to Linux Mint.

## In parallel

- [ ] **The Long Climb** (Minecraft modpack): manage as a project with its own stages and next steps.
- [ ] **Skills growth and evaluation:** complete Survey 1, then Survey 2; update `assets/expertise.yaml`
  history after each evaluation; revisit the learning path.
- [ ] **Optional: preparing to offer services.** Revisit after Survey 1 clarifies goals and timing.

## Open questions

1. What exactly defines "working order" for Client and Headless?
2. Backup method and tools: to be decided and recorded in `docs/decisions/`.
3. What role does system-snapshot software play next to real backups? Snapshots protect against
   a bad update; they do not protect against losing the drive or the machine.
4. Order of "Next" and "Later" items after Survey 1 results.

## Change log

- 2026-11-02: first draft from stated priorities.

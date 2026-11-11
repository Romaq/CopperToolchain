# Design maxims

A mental post-it note: short phrases that come to mind at the moment of a snap judgement.
They inform risk assessment in every project. The five-question checklist for adding
services lives next to this file in `can-vs-should.md`.

Good judgement comes from experience, and experience comes from bad judgement. I may not
remember the details of a bad experience, but I can keep the lesson in a phrase that is
easy to recall.

## Snap-judgement index

| The moment | Reach for |
|---|---|
| About to add a service or tool | Could vs should; the wheel |
| About to build something that already exists | The wheel |
| Every option looks bad | Sometimes all options suck |
| Tempted to polish before it works | Make it work first |
| About to try something new on a live system | Bad judgement cheap; big grenades; exits |
| A long run of green checks | Plans going well |
| An automation I will not look at again | Fire and forget |
| Someone is relying on my tool | Easy for you |

## Our own maxims

How to add one: a phrase, an "Applied as" line, and (optional) the decision record or
incident it came from. Keep each entry short enough to read at a glance.

### Make mistakes hard to make, easy to catch, and easy to correct
Prefer simple, scripted automation over manual tracking.

### Good judgement comes from experience; experience comes from bad judgement
Applied as: make bad judgement cheap. Practise in scratch repos with fake values, keep backups,
and prefer steps that can be undone.

### "Your scientists were so preoccupied with whether they could, they didn't stop to think if they should" -- Ian Malcolm, Jurassic Park (1993)
Applied as: `can-vs-should.md` holds the five rules for adding services to the Home Lab.
Ask them before the service exists, not after it needs maintenance.

### Sometimes all options suck
Applied as: stop shopping and choose the least bad option. Searching for a perfect one costs
time, which is the scarcest resource. To choose:
1. Which is easiest to undo?
2. Which fails loudly instead of silently?
3. Which could I rebuild from a short written recipe?

Then pick, time-box it, write the decision down with a "Revisit if" trigger, and move on.
This is not a licence to skip backups, restore tests, or security updates. Those are part of
"working", not options to trade away.

### Make it work, then worry about making it work better
Applied as: before starting, write one sentence defining "works", including how it will be
verified and that failure is visible. Build that and stop. Improvements go on the parking lot
with a trigger that says when they become worth doing. A backup with an untested restore does
not yet work.

### Reinventing the wheel is generally a bad plan unless you make a very nice wheel
Applied as: before building, spend about thirty minutes looking for an existing tool and note
what was found in the decision record, including why it was rejected. Build only if I can name
what the nicer wheel gives me. Adopting an existing tool with a thin wrapper beats writing a
new one. Any tool that reads my private data gets the same trust check as a script: read the
source, and know where it sends data. Building something for the learning is legitimate, but
label it as learning and not as infrastructure.

## Borrowed maxims: Schlock Mercenary

*The Seventy Maxims of Maximally Effective Mercenaries* is a fictional handbook from the web
comic Schlock Mercenary by Howard Tayler, later published as a real book. Its maxims do what
these do, and in the comic they are quoted right before the characters repeat the mistake.
The author permits individual maxims to be referenced with credit, as if the book were real.

Credit: Howard Tayler, *Schlock Mercenary*. List and sources: <https://schlockmercenary.fandom.com/wiki/The_Seventy_Maxims_of_Maximally_Effective_Mercenaries>.
Entries below give the maxim's number and a gloss in our own words. The exact wording is in the
book. Numbers follow that wiki page; check them against the printed book.

### Maxim 14 (on mad science)
"Mad Science" means never stopping to ask "what's the worst thing that could happen?"
Applied as: ask it. It is rule 2 of `can-vs-should.md`.

### Maxim 17 (on plans going well)
The longer everything goes according to plan, the bigger the impending disaster.
Applied as: a long run of green checks is a reason to test the checks. Use a verifier that can
fail, and rehearse restores before they are needed.

### Maxim 26 (on fire and forget)
"Fire and Forget" is fine, provided you never actually forget.
Applied as: automation that I will not look at again needs an alert when it stops. Alert on
silence, not just on errors.

### Maxim 38 (on what is easy for you)
Just because it's easy for you doesn't mean it can't be hard on your clients.
Applied as: friends, family, and other projects using my tools do not share my setup.
Test the instructions from their side (for example, a Windows client without bash).

### Maxim 41 (on backups)
"Do you have a backup?" means "I can't fix this."
Applied as: the backup is the fix, so test the restore, once per class of host.

### Maxim 43 (on stupid but working)
If it's stupid and it works, it's still stupid and you're lucky.
Applied as: write down that a working solution was luck, and put a "Revisit if" line on it.

### Maxim 61 (on grenades and small rooms)
Don't bring big grenades into small rooms.
Applied as: scripts that run as root on the hypervisor have a wide blast radius. Read them
first and try them in a scratch container.

### Maxim 68 (on exits)
Negotiating from a position of strength does not mean you shouldn't also negotiate from a position near the exits.
Applied as: before a change, know how to go back (a snapshot, a backup, the old config copied aside).

### Maxim 70 (on failure). Failure is not an option - it is mandatory. The option is whether or not to let failure be the last thing you do. Applied as: There **will** be occasions where no workable solution appears available, an error causes a catastrophic halt to the project, or security is breached despite best efforts using best practices. Such events are non-optional. The option is to decide to continue anyway.

Candidates to add when a bad experience earns them: 42 (a plan nobody expects usually means
something stupid is about to be tried) and 52 and 53 (the army and the intel on hand are never
the ones I wanted, a companion to "all options suck").

---
name: canonical-tracker
description: Keep one canonical Markdown tracker as the record of a project and every derived glance surface (dashboard, status page, plan document) provably in agreement with it — batched syncs, script-only edits with exact-match asserts, glyph truth, honest denominators, a closed index, an append-only archive, and a mechanical sync check that grows with every stale surface it missed. Use it when a chat maintains a project tracker or status dashboard, when closing or opening a tracked item, when figures move, or when someone asks "are you sure the numbers are right?"
---

# The canonical tracker

A project has one **record** — a Markdown file that says what is open, what is done, what
the human owes, and what the numbers are. Everything else that shows those facts — a
dashboard, a status page, a plan document with a progress line, a project summary — is a
**glance surface**: derived from the record, never edited on its own, and never trusted to
agree with the record until a check has read both.

This skill is the discipline that keeps that true. Each rule was written after a glance
surface went stale in a way a reader would have been misled by. The last section is the
check that now catches those cases mechanically; extend it every time it misses one.

## 1. One record, many surfaces

- **The canonical tracker is the source of truth.** Figures, statuses, asks, decisions: if
  the canonical and a surface disagree, the surface is wrong by definition.
- **Surfaces are derived.** They are patched *from* the canonical, in the same batch, by
  the same chat. A surface is never the place a fact is first written.
- **The archive is append-only.** Narrative — the why, the rejected options, the evidence —
  lands there **once**, at close, and the canonical row points at it. The tracker stays
  readable because the story lives somewhere else.
- **One chat writes all of them.** Single writer per surface; the sync is one batch, one
  hand.

## 2. The sync batch, in order

1. Edit the canonical (section 3).
2. Patch every glance surface from it.
3. Run the sync check (section 7). **Red means stop — nothing ships until it is green.**
4. Publish the surfaces (send the file, update the hosted page, write the project doc).
5. Append to the archive if something closed.

**Batch discipline governs.** Sync at milestone close, decision checkpoint, session end, or
on request — not after every message. Write immediately only for a live defect, a security
or cost exposure, a decision that would otherwise be lost, or **a glance surface a reader
would be misled by**: a stale status symbol, a closed decision shown open, an ask already
answered still listed, a headline percentage three weeks old.

## 3. Edit by script, with exact-match asserts

Every edit to the canonical or a surface is a scripted replacement that **asserts the old
string occurs exactly once** before it writes:

```python
def rep(s, old, new, label):
    n = s.count(old); assert n == 1, "%s: found %d" % (label, n)
    return s.replace(old, new, 1)
```

- **Grep the exact current text first.** Never write a replacement from a guessed or
  remembered string; most historical failures were guessed strings.
- A script that throws before its write leaves the file untouched. After any assert
  failure, look at what actually landed before re-running.
- A replacement that ends mid-table-row can splice two rows together — grep for stray
  pipes after any structural edit.
- Write to a temp file and land by atomic replace.

`scripts/patch.py` does this from a JSON list of edits, all-or-nothing.

## 4. Glyph truth

The status symbol is part of the row's truth. When close text lands on a row, the symbol
flips **in the same edit** — a row whose words say closed while its symbol says open is
exactly the glance-lie the batching exceptions exist for. Conventions that have held up:

- ⬜ open · 🟡 in progress (work has started — *unblocked* is not *underway*) · ✅ done on
  proven evidence · ⏸️ deferred with a named trigger · ❌ dropped
- A closed row **leaves the open tables** and joins the closed index the same edit.
- **Promote or demote, never annotate.** A row that changes tier physically moves; a note
  saying "really this is deferred" on a row still sitting in the active table is a lie the
  reader has to discover.

## 5. Honest denominators

The headline percentage is only worth reading if its arithmetic is honest:

- **A new item on a feature ruling moves the denominator.** The headline dips; nothing
  regressed; say so on the figures row. Hiding committed work in a later tier to protect a
  percentage is the dishonest move.
- **Open → in progress never touches a numerator.** Only proven closes do.
- **A new item lands as not-started** and climbs the states as the work ships, so the
  by-state counts stay true.
- **A struck item is removed from the denominator and scrubbed everywhere** — every
  surface, every document, one content search across the repository — or it is not struck.
- **Counts must sum.** Done + in-progress + open + deferred + dropped = the stated total,
  and the check asserts it.
- **Only the human mints identifiers.** A chat that numbers its own findings turns the
  tracker into a holding pen; most findings are a momentary fix or a note on an existing
  row, and a numbered row is the rarest disposition.

Record every denominator move as a dated parenthetical on the figures row itself
(*"9-02: B65 ✅ 68→69"*), so the arithmetic is auditable from the record alone.

## 6. The reader's first screen

The canonical opens with, in this order: the figures table · **Needs you** (every ask of
the human, one line each, what it unblocks; dated asks are not restated before their date)
· state of play · then the tiers. The closed index carries its count in its heading, and the
check asserts that count against the rows beneath it — the heading is a glance surface too.

## 7. The sync check

`scripts/check_sync.py` reads the canonical as truth and asserts that every surface agrees.
It fails loudly and lists every mismatch. What it checks, from a small manifest:

- every figure in the figures table appears in each surface exactly where the manifest says
  (headline %, done-of-total, tier segments, stat tiles, subhead count)
- the counts row sums to its stated total
- the closed-index heading matches the number of closed rows
- every open key in the canonical appears in the surface's glance area
- optional: summary lines under a length cap (long prose belongs inside an expand), tag
  balance for HTML surfaces, deprioritized items sitting under the deprioritized heading

**A gate is worth exactly what its negative case can see.** Every assertion in the check was
added after a real stale surface got past a human read: a header three weeks old under fresh
numbers, a tier card carrying last week's figures, a closed-index heading ten rows behind.
When the check misses one, the fix is two moves — fix the surface, *then add the assertion*
— never the first alone. The gate grows by its misses.

## Setting up

1. Copy `templates/TRACKER.md` and `templates/ARCHIVE.md`; rename the tiers to yours.
2. Copy `templates/surfaces.json`, point it at your canonical and your surfaces, and write
   one needle per figure per surface (see the template for the placeholder names).
3. `python3 scripts/check_sync.py surfaces.json` — green before you edit anything.
4. From then on: edit → patch → check → publish → archive. Never publish red.

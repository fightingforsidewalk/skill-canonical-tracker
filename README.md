# canonical-tracker

**One record, many glance surfaces, and a check that proves they agree.**

A Claude skill for any chat that maintains a project tracker or status dashboard. Plain
Markdown record, script-only edits, honest arithmetic, and a small sync check that reads the
record as truth and fails loudly when any derived surface disagrees.

Companion to the **claude-relay** repo — the mailbox and operating model for
running one project across several chats. This repo is the third leg: how the record stays
true.

---

## The problem

When an AI maintains your tracker, the tracker looks maintained. Rows get long, notes get
added, the dashboard gets regenerated — and three weeks later you notice the headline
percentage in the page header is from a different month than the numbers under it. Nobody
lied. The chat patched what the latest message named and nothing forced it to look at the
rest.

That happened on a real product build, more than once: a header three weeks stale under
fresh figures; a tier summary carrying last week's counts after two new items were added; a
closed-items heading ten rows behind the rows beneath it. Every one was caught by the human
reading the page, which is exactly the wrong gate. A tracker's whole claim to be a record
rests on its glance surfaces being true, and only a check that reads the record and asserts
the surface can guarantee that.

## What's here

**`skills/canonical-tracker/SKILL.md`** — the discipline, with the reasons:

- **One record, many surfaces.** The canonical Markdown tracker is the source of truth;
  dashboards, status pages and plan documents are derived and patched from it in one batch.
- **Edit by script, exact-match asserts.** Every edit asserts the old string occurs exactly
  once before it writes. Grep first; never write a replacement from memory.
- **Glyph truth.** The status symbol flips in the same edit as the words. Promote or demote
  a row by moving it — never by annotating it in place.
- **Honest denominators.** A new item on a feature ruling moves the denominator and the
  headline dips — say so. Open → in-progress never touches a numerator. Counts must sum.
  A struck item is scrubbed everywhere or it is not struck. Only the human mints identifiers.
- **Needs you first.** The human's asks are the first thing on the page, one line each,
  never restated before their date.
- **The archive is append-only** and the closed index carries its count in its heading —
  which the check asserts, because the heading is a glance surface too.
- **The check grows by its misses.** When a stale surface gets past it, fix the surface
  *and* add the assertion. Never the first alone.

**`scripts/check_sync.py`** — reads the figures table from the canonical, fills a manifest
of needles, and asserts every surface contains them; also checks the counts row sums, the
closed-index heading matches its rows, every open key appears in the surface's glance area,
and (optionally) summary-line length, HTML tag balance, and that deprioritized items sit
under the deprioritized heading. Red means nothing ships.

**`scripts/patch.py`** — exact-match edits from a JSON list, all-or-nothing, atomic.

**`templates/`** — a canonical `TRACKER.md` (figures table, Needs you, state of play,
tiers, deprioritized, closed index, decisions, open questions), an `ARCHIVE.md`, and a
`surfaces.json` manifest showing the placeholder names.

## Let your Claude adopt it for you

The fastest path is [`ADOPT.md`](ADOPT.md): one prompt you paste into a Claude that can see
this repo. It reads the skill, explains it back, asks you five setup questions, installs the
skill the way your session allows, creates the tracker, wires the check, makes it fail once
on purpose, and tells you the sync batch. Other assistants: [`USING-WITH-OTHER-AIS.md`](USING-WITH-OTHER-AIS.md).

## Quick start

```bash
cp -r skills/canonical-tracker/templates/* my-project/docs/
cd my-project/docs
# edit TRACKER.md; point surfaces.json at your dashboard / status page; write one needle per figure
python3 ../../skills/canonical-tracker/scripts/check_sync.py surfaces.json
```

```
sync check clean — every surface agrees with the canonical
```

Break something on purpose first — change one number on the dashboard — and watch it go
red. **A gate is worth exactly what its negative case can see.** A check you have never
seen fail has not been proven to exist.

## The sync batch

1. Edit the canonical (by script, exact match).
2. Patch every glance surface from it.
3. `check_sync.py` — green, or stop.
4. Publish the surfaces.
5. Append to the archive if something closed.

Batch at milestone close, decision checkpoint, session end, or on request — not after every
message. Write immediately only for a live defect, a security or cost exposure, a decision
that would otherwise be lost, or a glance surface a reader would be misled by.

## Installing the skill

**Claude Code** — copy `skills/canonical-tracker/` into `.claude/skills/` (or
`~/.claude/skills/`). **Claude.ai / desktop** — zip the folder and upload it under
*Settings → Capabilities → Skills*. **Anywhere else** — `SKILL.md` is plain Markdown; paste
it into the project's instructions.

## Layout

```
ADOPT.md                  a prompt that lets your Claude adopt this for you
USING-WITH-OTHER-AIS.md   ChatGPT, Gemini, mixed setups
skills/canonical-tracker/
  SKILL.md
  scripts/check_sync.py     the gate
  scripts/patch.py          exact-match edits, all-or-nothing
  templates/TRACKER.md      the canonical record
  templates/ARCHIVE.md      append-only narrative
  templates/surfaces.json   the manifest: which figures, which needles, which surfaces
examples/
  denominator-moves.md      the arithmetic, worked
```

## License

CC0 1.0 Universal (public domain dedication). The rules are the useful part; the scripts are small, and rewriting them for your
own surfaces is probably the right move.

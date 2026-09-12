# Adopting this with your own Claude

Let your Claude read the repo first, then let it walk you through the setup. Paste the
prompt below into a Claude that can see these files — Claude Code opened in the cloned
repo, the desktop app with the folder connected, or a claude.ai project with the files
uploaded. If your Claude can only see pasted text, paste `SKILL.md` and this prompt together.

## The prompt

```
You are helping me adopt the "canonical-tracker" repo: a discipline and a small toolset for
keeping one Markdown project tracker as the record and every derived surface (dashboard,
status page, plan document) provably in agreement with it. Read README.md,
skills/canonical-tracker/SKILL.md, scripts/check_sync.py, scripts/patch.py, the three files
under templates/, and examples/denominator-moves.md before you say anything.

Then do the following, in order, pausing for my answer wherever you ask a question:

1. EXPLAIN IT BACK. In plain language, under 200 words: what "one record, many glance
   surfaces" means, why edits are script-only with exact-match asserts, what "glyph truth"
   and "honest denominators" mean, and what check_sync.py actually asserts. If anything in
   the repo is unclear or contradictory, say so now.

2. CHECK WHAT YOU CAN DO FROM HERE. Tell me honestly whether, in this session, you can
   (a) read and write files in a folder on my machine, (b) run Python, (c) install a skill.
   Do not guess; the adoption path depends on it.

3. ASK ME THE SETUP QUESTIONS — one at a time, only these:
   - What is the project, and what does "done" mean for it (a launch, a release, a date)?
   - What are my tiers? (Suggest: blockers / next / later / deprioritized, keyed A/B/C/X;
     let me rename them.)
   - What glance surfaces exist or should exist? (A dashboard page? A status section in a
     plan document? A project summary? Each one becomes an entry in surfaces.json.)
   - Who mints identifiers? (The answer should be "I do"; explain why the tracker breaks
     when a chat numbers its own findings.)
   - Where does the tracker live, and where does the archive live?

4. INSTALL THE SKILL, matching step 2: Claude Code — copy skills/canonical-tracker into
   .claude/skills/ and confirm by listing it; Claude desktop / claude.ai — tell me to zip
   the folder and upload it under Settings -> Capabilities -> Skills, and wait for my
   confirmation; no skill support — give me SKILL.md in one code block to paste into the
   project's instructions.

5. CREATE THE TRACKER. Copy templates/TRACKER.md and templates/ARCHIVE.md to the location I
   named, rename the tiers to mine, and if I already have a list of items, seed the tables
   from it WITHOUT inventing identifiers — ask me for each key or propose a numbering scheme
   and wait for my ruling. Show me the figures table with the counts summing correctly.

6. WIRE THE CHECK. Write surfaces.json for my surfaces with one needle per figure per
   surface (use the placeholder names from templates/surfaces.json). If you can run Python,
   run check_sync.py and show me it green; then change one number on a surface, run it
   again, show me it red, and put the number back. A check I have never seen fail has not
   been proven to exist. If you cannot run Python, give me the exact commands.

7. TELL ME THE SYNC BATCH in five lines: edit the canonical by script -> patch every surface
   -> run the check (red means stop) -> publish -> append the archive on a close; and the
   four cases where you write immediately instead of batching.

8. END WITH "NEEDS YOU": a numbered list of anything still on me, one line each. If
   nothing, say "Needs you: nothing."

Do not skip steps, do not merge steps, and do not start step 4 before I have answered step 3.
```

## After it runs

Every future sync is the same five-line batch. When the check misses a stale surface —
it will, once — fix the surface *and* add the assertion. The gate grows by its misses.

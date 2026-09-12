# Using this with ChatGPT, Gemini, or anything else

Nothing here is Claude-specific. The "skill" is a Markdown file of instructions; the
tracker is a Markdown file; the check and the patcher are plain Python.

| The assistant needs to… | Claude Code / desktop | claude.ai project | ChatGPT / Gemini / other |
|---|---|---|---|
| know the discipline | install the skill, or paste SKILL.md into instructions | paste SKILL.md into project instructions | paste SKILL.md into the custom instructions / system prompt |
| edit the tracker and surfaces | edits files directly, by script | gives you the edited file or the patch.py edits.json to apply | with file access: directly; otherwise gives you the text |
| run check_sync.py before publishing | yes | you run it | with a code tool that can see your folder: yes; otherwise you run it |

The one thing that must not degrade across tools is **the check runs before anything is
published**. If the assistant cannot run it, you run it — `python3 check_sync.py
surfaces.json` takes a second — and you paste the result back. A tracker whose surfaces are
never checked against the record is exactly the thing this repo exists to prevent.

The other thing to keep identical: **only the human mints identifiers**, whatever tool the
assistant runs in. Every assistant will offer to number its findings. Decline.

#!/usr/bin/env python3
"""patch.py — exact-match edits, all-or-nothing, atomic.

    python3 patch.py FILE edits.json

edits.json is a list of {"label": "...", "old": "...", "new": "..."}. Every "old" must occur
EXACTLY once in FILE or nothing is written — a script that throws before its write leaves
the file untouched. Grep the exact current text before writing an edit; never write one
from a remembered string.
"""
import io, json, os, sys


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    path, edits_path = sys.argv[1], sys.argv[2]
    s = io.open(path, encoding="utf-8").read()
    edits = json.load(io.open(edits_path, encoding="utf-8"))
    for e in edits:
        n = s.count(e["old"])
        if n != 1:
            sys.exit("%s: old string found %d times, expected 1 — nothing written" % (e.get("label", "?"), n))
        s = s.replace(e["old"], e["new"], 1)
    tmp = path + ".tmp"
    io.open(tmp, "w", encoding="utf-8").write(s)
    os.replace(tmp, path)
    print("%d edit(s) applied to %s" % (len(edits), path))


if __name__ == "__main__":
    main()

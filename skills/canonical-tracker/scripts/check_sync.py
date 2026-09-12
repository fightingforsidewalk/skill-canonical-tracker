#!/usr/bin/env python3
"""check_sync.py — fail loudly when a glance surface disagrees with the canonical tracker.

    python3 check_sync.py surfaces.json

The manifest names the canonical file, which figure rows to read, and for each surface a
list of needle templates that must appear in it once the placeholders are filled from the
canonical. Placeholders: {<figure>.pct} {<figure>.done} {<figure>.total} and
{counts.done} {counts.prog} {counts.open} {counts.defer} {counts.drop} {counts.total}.

Run it before EVERY sync. A gate is worth exactly what its negative case can see — this
script reads the canonical as the source of truth and asserts the surfaces agree, rather
than trusting that an edit happened. When it misses a stale surface, add the assertion.
"""
import io, json, re, sys

fail = []


def read(p):
    return io.open(p, encoding="utf-8").read()


def figure_row(canon, label):
    m = re.search(r"\|\s*\*\*" + re.escape(label) + r"\*\*\s*\|\s*\*\*(\d+)%\*\*\s*—\s*(\d+) of (\d+)", canon)
    if not m:
        fail.append("canonical: cannot read figure row %r" % label)
        return None
    return {"pct": int(m.group(1)), "done": int(m.group(2)), "total": int(m.group(3))}


def counts_row(canon, glyphs):
    pat = r"\|\s*\*\*Counts\*\*\s*\|\s*" + r"\s*·\s*".join(r"(\d+)\s*" + re.escape(g) for g in glyphs) + r"\s*·\s*(\d+)\s*(?:parent|item)"
    m = re.search(pat, canon)
    if not m:
        fail.append("canonical: cannot read the Counts row (glyph order in manifest must match the file)")
        return None
    nums = list(map(int, m.groups()))
    parts, total = nums[:-1], nums[-1]
    if sum(parts) != total:
        fail.append("canonical: counts sum to %d, not the stated %d" % (sum(parts), total))
    keys = ["done", "prog", "open", "defer", "drop"][: len(parts)]
    d = dict(zip(keys, parts))
    d["total"] = total
    return d


def closed_index(canon):
    m = re.search(r"^## .*?\((\d+) items?\)\s*$", canon, re.M)
    if not m:
        return
    sec = canon[m.end():]
    sec = sec[: sec.find("\n## ")] if "\n## " in sec else sec
    rows = len(re.findall(r"^\|\s*[A-Z]+\d+\s*\|", sec, re.M))
    if rows != int(m.group(1)):
        fail.append("closed-index heading says %s items, section holds %d rows" % (m.group(1), rows))


def open_keys(canon, key_re):
    """Keys of rows in the open tables: a row whose ID cell is followed by a bold item cell."""
    return re.findall(r"^\|\s*(" + key_re + r")\s*\|\s*\*\*", canon, re.M)


def check_surface(sf, values, canon, cfg):
    html = read(sf["file"])
    name = sf["file"]
    for needle in sf.get("needles", []):
        try:
            filled = needle.format(**values)
        except KeyError as e:
            fail.append("%s: needle %r uses unknown placeholder %s" % (name, needle, e))
            continue
        if filled not in html:
            fail.append("%s: missing %r" % (name, filled))
    if "open_keys_within" in sf:
        for k in open_keys(canon, cfg.get("key_regex", r"[A-Z]+\d+")):
            if k not in html[: sf["open_keys_within"]]:
                fail.append("%s: open row %s missing from the glance area (first %d chars)" % (name, k, sf["open_keys_within"]))
    for tag in sf.get("balanced_tags", []):
        if len(re.findall(r"<%s\b" % tag, html)) != html.count("</%s>" % tag):
            fail.append("%s: unbalanced <%s>" % (name, tag))
    if "summary_regex" in sf and "summary_max" in sf:
        overs = [m for m in re.finditer(sf["summary_regex"], html, re.S)
                 if len(re.sub(r"<[^>]+>", "", m.group(1))) > sf["summary_max"]]
        if overs:
            fail.append("%s: %d summary lines over %d visible chars — move the prose inside the expand"
                        % (name, len(overs), sf["summary_max"]))
    for k in sf.get("deprioritized_keys", []):
        i = html.find('"id">%s<' % k)
        if i == -1:
            continue
        heads = [m for m in re.finditer(r"<h2[^>]*>(.*?)</h2>", html, re.S) if m.start() < i]
        if heads and sf.get("deprioritized_heading", "Deprioritized") not in heads[-1].group(1):
            fail.append("%s: %s sits under %r, not the deprioritized section"
                        % (name, k, re.sub(r"<[^>]+>", "", heads[-1].group(1)).strip()))


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    cfg = json.load(io.open(sys.argv[1], encoding="utf-8"))
    canon = read(cfg["canonical"])
    values = {}
    for key, label in cfg.get("figures", {}).items():
        row = figure_row(canon, label)
        if row:
            for k, v in row.items():
                values["%s.%s" % (key, k)] = v
    counts = counts_row(canon, cfg.get("count_glyphs", ["✅", "🟡", "⬜", "⏸️", "❌"]))
    if counts:
        for k, v in counts.items():
            values["counts.%s" % k] = v
    if cfg.get("check_closed_index", True):
        closed_index(canon)
    # str.format wants flat names: allow {progress.pct} by mapping dotted keys onto a dict subclass
    class Dotted(dict):
        def __missing__(self, k):
            raise KeyError(k)
    flat = Dotted(values)
    for sf in cfg.get("surfaces", []):
        # translate {a.b} -> {a_b} for str.format
        sf2 = dict(sf)
        sf2["needles"] = [re.sub(r"\{(\w+)\.(\w+)\}", r"{\1_\2}", n) for n in sf.get("needles", [])]
        check_surface(sf2, {k.replace(".", "_"): v for k, v in flat.items()}, canon, cfg)
    if fail:
        print("SYNC CHECK FAILED (%d)" % len(fail))
        for f in fail:
            print("  ✗", f)
        sys.exit(1)
    print("sync check clean — every surface agrees with the canonical")


if __name__ == "__main__":
    main()

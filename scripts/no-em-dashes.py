#!/usr/bin/env python3
"""Rewrite em dashes in visible copy. Tiago does not write with them.

Covers the text nodes of every page (not <head>, <script>, <style>, comments
or attributes, so titles, meta descriptions and schema stay as they are) and
the repo-hosted blog posts. Rules, in order:
  "$1M — $2M" / "9 — 5"     → " to "   (a range)
  "word — Capitalised"      → ": "     (a lead-in to a new clause or name)
  "word — word"             → ", "
  dash at the start/end of a text run → dropped
"""
import glob, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DASH = r"(?:—|&mdash;)"

def fix_text(t):
    if re.fullmatch(r"\s*" + DASH + r"\s*", t):
        return t  # a lone dash is a value placeholder ("—" until data loads), not prose
    t = re.sub(r"(\$?[\d.,]+[KkMm]?\+?)\s*" + DASH + r"\s*(\$?[\d.,]+)", r"\1 to \2", t)
    t = re.sub(r"(\S)\s*" + DASH + r"\s*(?=[A-Z])", r"\1: ", t)
    t = re.sub(r"(\S)\s*" + DASH + r"\s*(?=\S)", r"\1, ", t)
    t = re.sub(r"^\s*" + DASH + r"\s*", "", t)
    t = re.sub(r"\s*" + DASH + r"\s*$", "", t)
    return t

def fix_html(doc):
    head_end = doc.find("<body")
    head, body = (doc[:head_end], doc[head_end:]) if head_end > 0 else ("", doc)
    protected = re.compile(r"<script\b.*?</script>|<style\b.*?</style>|<!--.*?-->|<[^>]+>", re.S)
    out, pos = [], 0
    for m in protected.finditer(body):
        out.append(fix_text(body[pos:m.start()])); out.append(m.group(0)); pos = m.end()
    out.append(fix_text(body[pos:]))
    return head + "".join(out)

def main():
    changed = 0
    for f in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
        if os.path.basename(f) in ("admin.html", "admin-import.html"): continue
        doc = open(f, encoding="utf-8").read(); new = fix_html(doc)
        if new != doc: open(f, "w", encoding="utf-8").write(new); changed += 1
    p = os.path.join(ROOT, "blog-posts-local.json"); rows = json.load(open(p, encoding="utf-8")); n = 0
    for r in rows:
        for k in ("title", "excerpt", "body"):
            if isinstance(r.get(k), str) and ("—" in r[k]):
                r[k] = "\n".join(fix_text(line) for line in r[k].split("\n")); n += 1
    json.dump(rows, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False); open(p, "a").write("\n")
    print(f"pages changed: {changed}; post fields changed: {n}")

if __name__ == "__main__": sys.exit(main())

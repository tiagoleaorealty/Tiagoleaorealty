#!/usr/bin/env python3
"""Inline design.css into every page and wire up the Cormorant font.

Each page carries its own <style> block, so shared styling has to be copied
into each one. This script does that copy, idempotently:

  * design.css is inserted at the END of each page's first <style> block,
    between DESIGN-POLISH markers (re-running replaces the old copy), so its
    rules win over the page's own rules at equal specificity.
  * A Google Fonts link for Cormorant Garamond (regular 400/500 + italic 400,
    display=swap) goes in right after the fonts.css link, with preconnects.
  * The white nav backgrounds become the cream page tint.

Run from the repo root after editing design.css:  python3 scripts/apply-design.py
Templates (property-detail.html, blog-post.html, school.html, development.html)
are covered, so the pages build.py bakes from them pick it up on the next build.
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START = "/* ==== DESIGN POLISH ===="
END = "/* ==== /DESIGN POLISH ==== */"
FONT_LINKS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&display=swap">'
)
SKIP = {"admin.html", "admin-import.html", "404.html"}


def pages():
    out = [f for f in sorted(glob.glob(os.path.join(ROOT, "*.html"))) if os.path.basename(f) not in SKIP]
    return out


def inline_polish(doc, css):
    # Replace an existing copy, else append inside the first <style> block.
    if START in doc:
        i = doc.index(START)
        j = doc.index(END) + len(END)
        return doc[:i] + css.strip() + doc[j:]
    m = re.search(r"<style[^>]*>.*?</style>", doc, re.S)
    if not m:
        raise SystemExit("no <style> block")
    close = m.end() - len("</style>")
    return doc[:close] + "\n" + css.strip() + "\n  " + doc[close:]


def add_fonts(doc):
    if "fonts.googleapis.com/css2?family=Cormorant" in doc:
        return doc
    m = re.search(r'<link rel="stylesheet" href="fonts\.css"\s*/?>', doc)
    if not m:
        return doc
    return doc[:m.end()] + "\n  " + FONT_LINKS + doc[m.end():]


def tint_nav(doc):
    # nav { background: rgba(255,255,255,.92) } → the cream page tint
    def fix(m):
        return re.sub(r"rgba\(255,\s*255,\s*255,\s*(0?\.\d+)\)", r"rgba(247,244,239,\1)", m.group(0))
    return re.sub(r"\n\s*nav(?:\.scrolled)?\s*\{[^}]*\}", fix, doc)


def main():
    css = open(os.path.join(ROOT, "design.css"), encoding="utf-8").read()
    if START not in css or END not in css:
        raise SystemExit("design.css is missing its DESIGN POLISH markers")
    n = 0
    for f in pages():
        doc = open(f, encoding="utf-8").read()
        new = tint_nav(add_fonts(inline_polish(doc, css)))
        if new != doc:
            open(f, "w", encoding="utf-8").write(new)
            n += 1
    print(f"design applied to {n} page(s)")


if __name__ == "__main__":
    sys.exit(main())

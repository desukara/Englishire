#!/usr/bin/env python3
"""Export every English/Japanese human-readable string pair for editorial review."""
from __future__ import annotations

import csv
from pathlib import Path
from bs4 import BeautifulSoup, Comment

ROOT = Path(__file__).resolve().parents[1]
JA = ROOT / "ja"
OUT = ROOT / "scripts" / "translation_audit.tsv"
PAGES = [
    "index.html", "teacher-cover.html", "how-it-works.html",
    "englishire-standard.html", "questions.html", "contact.html",
    "about.html", "service-standards.html", "privacy.html", "cookies.html",
    "terms.html", "accessibility.html", "editorial-policy.html",
    "permissions.html", "thank-you.html",
]
SKIP = {"script", "style", "code", "pre", "svg", "path"}
ATTRS = ("title", "aria-label", "alt", "placeholder")


def clean(value: str) -> str:
    return " ".join(value.split())


def visible_nodes(soup: BeautifulSoup):
    for node in soup.find_all(string=True):
        if isinstance(node, Comment) or not node.parent or node.parent.name in SKIP:
            continue
        value = clean(str(node))
        if value:
            yield ("text", node.parent.name, value)
    for tag in soup.find_all(True):
        for attr in ATTRS:
            if tag.has_attr(attr):
                value = clean(str(tag.get(attr, "")))
                if value:
                    yield (f"attr:{attr}", tag.name, value)
    for meta in soup.select('meta[name="description"], meta[property^="og:"], meta[name^="twitter:"]'):
        value = clean(str(meta.get("content", "")))
        if value:
            yield ("meta", str(meta.get("name") or meta.get("property") or ""), value)


rows = []
for page in PAGES:
    en = BeautifulSoup((ROOT / page).read_text(encoding="utf-8"), "html.parser")
    ja = BeautifulSoup((JA / page).read_text(encoding="utf-8"), "html.parser")
    en_nodes = list(visible_nodes(en))
    ja_nodes = list(visible_nodes(ja))
    if len(en_nodes) != len(ja_nodes):
        raise SystemExit(f"{page}: visible node mismatch {len(en_nodes)} != {len(ja_nodes)}")
    for index, (left, right) in enumerate(zip(en_nodes, ja_nodes), start=1):
        kind, element, source = left
        ja_kind, ja_element, target = right
        if (kind, element) != (ja_kind, ja_element):
            raise SystemExit(f"{page}:{index}: node mismatch {(kind, element)} != {(ja_kind, ja_element)}")
        rows.append((page, index, kind, element, source, target))

with OUT.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(("page", "index", "kind", "element", "english", "japanese"))
    writer.writerows(rows)

print(f"Exported {len(rows)} aligned translation units to {OUT}")

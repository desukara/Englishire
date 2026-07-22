#!/usr/bin/env python3
"""Fail when canonical English source text lacks a reviewed Japanese translation."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup, Comment

from japanese_strict import STRICT_OVERRIDES

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "scripts" / "missing_strict_sources.tsv"
PAGES = [
    "index.html", "teacher-cover.html", "how-it-works.html",
    "englishire-standard.html", "questions.html", "contact.html",
    "about.html", "service-standards.html", "privacy.html", "cookies.html",
    "terms.html", "accessibility.html", "editorial-policy.html",
    "permissions.html", "thank-you.html",
]
SKIP_TAGS = {"script", "style", "code", "pre", "svg", "path"}
TRANSLATABLE_ATTRS = ("title", "aria-label", "alt", "placeholder", "value")
JSON_TRANSLATABLE_KEYS = {
    "name", "description", "serviceType", "headline", "alternativeHeadline",
    "caption", "articleSection", "keywords", "text",
}
ALLOWED_EXACT = {
    "html", "website", "article", "summary_large_image", "index, follow",
    "Englishire", "Englishire Journal", "Journal", "Tokyo", "ENGLISHIRE",
    "Formspree", "WCAG", "Email", "English", "Japanese",
    "info@englishire.com", "©", ".",
}


def normalise(value: str) -> str:
    return " ".join(value.split())


def is_technical_or_protected(source: str) -> bool:
    value = source.strip()
    if not value or value in ALLOWED_EXACT:
        return True
    if not re.search(r"[A-Za-z]", value):
        return True
    if value.startswith(("http://", "https://", "mailto:")):
        return True
    if re.fullmatch(r"[A-Z0-9_.@+\-/]+", value) and " " not in value:
        return True
    return False


def json_strings(value: Any, key: str | None = None):
    if isinstance(value, dict):
        for child_key, child in value.items():
            yield from json_strings(child, child_key)
    elif isinstance(value, list):
        for child in value:
            yield from json_strings(child, key)
    elif isinstance(value, str) and key in JSON_TRANSLATABLE_KEYS:
        source = normalise(value)
        if source:
            yield source


def page_sources(page: str):
    soup = BeautifulSoup((ROOT / page).read_text(encoding="utf-8"), "html.parser")

    for node in soup.find_all(string=True):
        if isinstance(node, Comment) or not node.parent or node.parent.name in SKIP_TAGS:
            continue
        source = normalise(str(node))
        if source:
            yield ("text", node.parent.name, source)

    for tag in soup.find_all(True):
        for attr in TRANSLATABLE_ATTRS:
            if tag.has_attr(attr):
                source = normalise(str(tag.get(attr, "")))
                if source:
                    yield (f"attr:{attr}", tag.name, source)

    for meta in soup.select('meta[name="description"], meta[property^="og:"], meta[name^="twitter:"]'):
        source = normalise(str(meta.get("content", "")))
        if source:
            yield ("meta", str(meta.get("name") or meta.get("property") or ""), source)

    for tag in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            data = json.loads(tag.string or "")
        except Exception:
            continue
        for source in json_strings(data):
            yield ("json-ld", "script", source)


missing: list[tuple[str, str, str, str]] = []
seen: set[str] = set()
for page in PAGES:
    for kind, element, source in page_sources(page):
        if source in seen or is_technical_or_protected(source):
            continue
        seen.add(source)
        if source not in STRICT_OVERRIDES:
            missing.append((page, kind, element, source))

with REPORT.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(("page", "kind", "element", "english"))
    writer.writerows(missing)

if missing:
    print(f"Strict Japanese coverage failed: {len(missing)} English source strings are unreviewed.")
    for page, kind, element, source in missing:
        print(f"- {page} [{kind} {element}]: {source}")
    raise SystemExit(1)

print(f"Strict Japanese coverage passed for {len(PAGES)} canonical pages and {len(STRICT_OVERRIDES)} reviewed source strings.")

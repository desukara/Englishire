#!/usr/bin/env python3
"""Fail when a translatable site string lacks a reviewed source-keyed translation."""
from __future__ import annotations

import csv
import re
from pathlib import Path

from japanese_strict import STRICT_OVERRIDES

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "scripts" / "translation_audit.tsv"

ALLOWED_EXACT = {
    "html", "website", "article", "summary_large_image", "index, follow",
    "Englishire", "Englishire Journal", "Journal", "Tokyo", "ENGLISHIRE",
    "Formspree", "WCAG", "Email", "info@englishire.com", "©", ".",
}


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


missing: list[tuple[str, str, str, str]] = []
with AUDIT.open(encoding="utf-8", newline="") as handle:
    for row in csv.DictReader(handle, delimiter="\t"):
        source = row["english"].strip()
        if is_technical_or_protected(source):
            continue
        if source not in STRICT_OVERRIDES:
            missing.append((row["page"], row["kind"], row["element"], source))

unique: list[tuple[str, str, str, str]] = []
seen: set[str] = set()
for item in missing:
    if item[3] in seen:
        continue
    seen.add(item[3])
    unique.append(item)

if unique:
    print(f"Strict Japanese coverage failed: {len(unique)} English source strings are unreviewed.")
    for page, kind, element, source in unique:
        print(f"- {page} [{kind} {element}]: {source}")
    raise SystemExit(1)

print(f"Strict Japanese coverage passed: {len(STRICT_OVERRIDES)} reviewed source strings loaded.")

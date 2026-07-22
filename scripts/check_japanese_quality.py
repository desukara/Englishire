#!/usr/bin/env python3
"""Fail on known Japanese translation corruptions and protected identifiers."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
JA = ROOT / "ja"

BANNED = {
    "info@englishshire.com": "info@englishire.com",
    "イングリッシュアイレ": "Englishire",
    "英語IRE": "Englishire",
    "© 2026 英語です。": "© 2026 Englishire.",
    "英語です。無断転載を禁じます。": "Englishire. 無断転載を禁じます。",
    "教師の補償": "講師の代講",
    "英語教師の補償": "英語講師の代講",
    "教師の表紙": "講師手配",
    "採用ギャップ": "採用までの空白期間",
    "仕事を見つけるまで": "学校が新しい講師を採用するまで",
    "新しい仕事を見つけるまで": "学校が新しい講師を採用するまで",
}

errors = []
for path in sorted(JA.glob("*.html")):
    text = path.read_text(encoding="utf-8")
    if "info@englishire.com" in text and "mailto:info@englishire.com" not in text:
        errors.append(f"{path.name}: visible contact email is not paired with the correct mailto link")
    for bad, preferred in BANNED.items():
        if bad in text:
            errors.append(f"{path.name}: found {bad!r}; expected {preferred!r}")

if errors:
    print("Japanese quality audit failed:", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(f"Japanese quality audit passed for {len(list(JA.glob('*.html')))} HTML files.")

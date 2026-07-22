#!/usr/bin/env python3
"""Validate Japanese parity while allowing the intentional language notice."""
from __future__ import annotations

from pathlib import Path

from bs4 import BeautifulSoup

import check_japanese_parity as parity

ROOT = Path(__file__).resolve().parents[1]
SERVICE_PAGES = {
    "index.html", "teacher-cover.html", "how-it-works.html",
    "questions.html", "contact.html", "service-standards.html", "terms.html",
}
NOTICE_TEXT = (
    "言語対応について "
    "日本語でのお問い合わせは、フォームまたはメールで承ります。"
    "電話、オンライン会議、対面での業務上のやり取りは英語で行います。"
    "日本語の文面作成には翻訳支援を使用する場合があります。"
)

errors: list[str] = []
for page in sorted(SERVICE_PAGES):
    path = ROOT / "ja" / page
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    notices = soup.select(".language-notice--service-boundary")
    if len(notices) != 1:
        errors.append(f"{page}: expected one service-language notice, found {len(notices)}")
        continue
    actual = " ".join(notices[0].stripped_strings)
    if actual != NOTICE_TEXT:
        errors.append(f"{page}: service-language notice text changed: {actual!r}")

if errors:
    print("Japanese release audit failed:")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

original_parse = parity.parse


def parity_parse(path: Path):
    doc = original_parse(path)
    if path.parent.name == "ja":
        for notice in doc.select(".language-notice--service-boundary"):
            notice.decompose()
    return doc


parity.parse = parity_parse
parity.main()
print(f"Japanese service-language boundary passed for {len(SERVICE_PAGES)} pages.")

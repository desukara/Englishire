#!/usr/bin/env python3
"""Ensure contact-form implementation and policy statements remain consistent."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ENDPOINT = "https://formspree.io/f/xbdnydnb"

checks = {
    ROOT / "contact.html": [ENDPOINT],
    ROOT / "ja" / "contact.html": [ENDPOINT],
    ROOT / "privacy.html": ["Formspree"],
    ROOT / "ja" / "privacy.html": ["Formspree"],
    ROOT / "cookies.html": ["Formspree"],
    ROOT / "ja" / "cookies.html": ["Formspree"],
}

banned = {
    ROOT / "cookies.html": [
        "The enquiry form prepares a message in the visitor's own email application.",
        "The website itself does not transmit or store the form entries.",
    ],
    ROOT / "ja" / "cookies.html": [
        "お問い合わせフォームは、利用者自身のメールアプリで送信するメッセージを作成します。",
        "ウェブサイト自体はフォームの入力内容を送信または保存しません。",
    ],
}

errors = []
for path, required in checks.items():
    if not path.exists():
        errors.append(f"missing required file: {path.relative_to(ROOT)}")
        continue
    text = path.read_text(encoding="utf-8")
    for value in required:
        if value not in text:
            errors.append(f"{path.relative_to(ROOT)}: missing required reference {value!r}")

for path, forbidden in banned.items():
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8")
    for value in forbidden:
        if value in text:
            errors.append(f"{path.relative_to(ROOT)}: contains obsolete statement {value!r}")

if errors:
    print("Form and policy consistency audit failed:", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Form and policy consistency audit passed.")

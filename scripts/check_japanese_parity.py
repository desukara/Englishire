#!/usr/bin/env python3
"""Fail when a Japanese page drifts structurally from its English source."""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

from bs4 import BeautifulSoup, Comment

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    "index.html", "teacher-cover.html", "how-it-works.html",
    "englishire-standard.html", "questions.html", "contact.html",
    "about.html", "service-standards.html", "privacy.html", "cookies.html",
    "terms.html", "accessibility.html", "editorial-policy.html",
    "permissions.html", "thank-you.html",
]

IGNORE_CLASSES = {"language-switch", "site-header__controls", "site-footer__language", "language-notice--service-boundary"}


def soup(path: Path) -> BeautifulSoup:
    return BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")


def structural_tokens(doc: BeautifulSoup) -> list[tuple]:
    tokens: list[tuple] = []
    for node in doc.descendants:
        if isinstance(node, Comment):
            continue
        name = getattr(node, "name", None)
        if not name:
            continue
        classes = tuple(sorted(c for c in node.get("class", []) if c not in IGNORE_CLASSES))
        attrs = []
        for key in ("id", "name", "type", "method", "required", "multiple", "min", "max", "step", "autocomplete"):
            if node.has_attr(key):
                attrs.append((key, str(node.get(key))))
        tokens.append((name, classes, tuple(attrs)))
    return tokens


def asset_names(doc: BeautifulSoup) -> Counter:
    values = []
    for tag, attr in (("img", "src"), ("source", "src"), ("source", "srcset"), ("script", "src"), ("link", "href")):
        for element in doc.find_all(tag):
            value = element.get(attr)
            if not value or str(value).startswith(("http://", "https://", "data:")):
                continue
            if tag == "link" and element.get("rel") and not set(element.get("rel", [])) & {"stylesheet", "icon", "manifest", "apple-touch-icon"}:
                continue
            values.append(Path(urlsplit(str(value)).path).name)
    return Counter(values)


def form_signature(doc: BeautifulSoup) -> list[tuple]:
    signature = []
    for form in doc.find_all("form"):
        controls = []
        for field in form.find_all(["input", "select", "textarea", "button"]):
            controls.append((field.name, field.get("name"), field.get("type"), field.has_attr("required")))
        signature.append((form.get("method", "get").lower(), tuple(controls)))
    return signature


def section_signature(doc: BeautifulSoup) -> list[tuple]:
    main = doc.find("main")
    if not main:
        return []
    result = []
    for section in main.find_all(["section", "article", "aside"], recursive=True):
        if "language-notice--service-boundary" in section.get("class", []):
            continue
        result.append((section.name, tuple(sorted(section.get("class", []))), section.get("id")))
    return result


def check_pair(name: str) -> list[str]:
    errors = []
    en_path = ROOT / name
    ja_path = ROOT / "ja" / name
    if not ja_path.exists():
        return [f"{name}: missing ja/{name}"]
    en, ja = soup(en_path), soup(ja_path)

    if ja.html.get("lang") != "ja":
        errors.append(f"{name}: Japanese html lang is not ja")
    if structural_tokens(en) != structural_tokens(ja):
        errors.append(f"{name}: DOM tag/class/form structure differs")
    if asset_names(en) != asset_names(ja):
        errors.append(f"{name}: images, stylesheets, scripts or icons differ")
    if form_signature(en) != form_signature(ja):
        errors.append(f"{name}: form controls or requirements differ")
    if section_signature(en) != section_signature(ja):
        errors.append(f"{name}: section/article sequence differs")

    en_ids = Counter(tag.get("id") for tag in en.find_all(id=True))
    ja_ids = Counter(tag.get("id") for tag in ja.find_all(id=True))
    if en_ids != ja_ids:
        errors.append(f"{name}: element IDs differ")

    # Localised pages must not accidentally point to the Japanese homepage for unrelated pages.
    for link in ja.find_all("a", href=True):
        href = str(link["href"])
        if href in {"index.html", "./", "/ja/"} and name != "index.html":
            label = " ".join(link.stripped_strings)
            if label not in {"Englishire", "ホーム", "ホームページ", "サービス案内"}:
                errors.append(f"{name}: suspicious unrelated homepage link: {label!r}")

    # Catch obviously untranslated prose while allowing brand names, email and Journal.
    visible = " ".join(
        str(node).strip() for node in ja.find_all(string=True)
        if node.parent and node.parent.name not in {"script", "style", "code", "pre"}
    )
    words = re.findall(r"\b[A-Za-z]{4,}\b", visible)
    allowed = {"Englishire", "Journal", "Tokyo", "Formspree", "Cookie", "WCAG", "Email", "English"}
    unexplained = [w for w in words if w not in allowed]
    if len(unexplained) > 20:
        errors.append(f"{name}: too much untranslated English prose remains ({len(unexplained)} words)")
    return errors


def main() -> None:
    errors = []
    for page in PAGES:
        errors.extend(check_pair(page))
    if errors:
        print("Japanese parity audit failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Japanese parity audit passed for {len(PAGES)} page pairs.")


if __name__ == "__main__":
    main()

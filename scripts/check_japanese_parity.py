#!/usr/bin/env python3
"""Fail when a Japanese page drifts from its canonical English counterpart."""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

from bs4 import BeautifulSoup, Comment, Doctype, NavigableString

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    "index.html", "teacher-cover.html", "how-it-works.html",
    "englishire-standard.html", "questions.html", "contact.html",
    "about.html", "service-standards.html", "privacy.html", "cookies.html",
    "terms.html", "accessibility.html", "editorial-policy.html",
    "permissions.html", "thank-you.html",
]

BANNED_TERMS = {
    "教師の補償": "講師の代講",
    "英語教師の補償": "英語講師の代講",
    "一時的な英語教師の補償": "英語講師の代講・短期手配",
    "教師の表紙": "講師手配",
    "採用ギャップ": "採用までの空白期間",
    "仕事を見つけるまで": "学校が新しい講師を採用するまで",
    "新しい仕事を見つけるまで": "学校が新しい講師を採用するまで",
    "英語IRE": "Englishire",
}

TECHNICAL_META = {
    ("property", "og:type"),
    ("name", "twitter:card"),
    ("name", "robots"),
}


def parse(path: Path) -> BeautifulSoup:
    text = path.read_text(encoding="utf-8")
    if not re.match(r"^<!DOCTYPE html>\s*<html", text, re.I):
        raise ValueError(f"{path}: malformed or missing HTML doctype")
    return BeautifulSoup(text, "html.parser")


def normalised_body_tokens(doc: BeautifulSoup) -> list[tuple]:
    body = doc.body
    if body is None:
        return []
    tokens: list[tuple] = []
    for node in body.descendants:
        if isinstance(node, (Comment, Doctype, NavigableString)):
            continue
        name = getattr(node, "name", None)
        if not name:
            continue
        classes = tuple(sorted(node.get("class", [])))
        attrs = []
        for key in (
            "id", "name", "type", "method", "enctype", "required", "multiple",
            "min", "max", "step", "autocomplete", "role",
        ):
            if node.has_attr(key):
                attrs.append((key, str(node.get(key))))
        tokens.append((name, classes, tuple(attrs)))
    return tokens


def section_signature(doc: BeautifulSoup) -> list[tuple]:
    main = doc.find("main")
    if not main:
        return []
    return [
        (tag.name, tuple(sorted(tag.get("class", []))), tag.get("id"))
        for tag in main.find_all(["section", "article", "aside"], recursive=True)
    ]


def asset_names(doc: BeautifulSoup) -> Counter:
    values = []
    for tag, attr in (
        ("img", "src"), ("source", "src"), ("source", "srcset"),
        ("script", "src"), ("link", "href"),
    ):
        for element in doc.find_all(tag):
            value = element.get(attr)
            if not value or str(value).startswith(("http://", "https://", "data:")):
                continue
            if tag == "link":
                rels = set(element.get("rel", []))
                if not rels & {"stylesheet", "icon", "manifest", "apple-touch-icon"}:
                    continue
            values.append(Path(urlsplit(str(value)).path).name)
    return Counter(values)


def form_signature(doc: BeautifulSoup) -> list[tuple]:
    result = []
    for form in doc.find_all("form"):
        controls = []
        for field in form.find_all(["input", "select", "textarea", "button", "option"]):
            controls.append((
                field.name,
                field.get("name"),
                field.get("type"),
                field.has_attr("required"),
                field.get("value") if field.name == "option" or str(field.get("type", "")).lower() in {"hidden", "checkbox", "radio"} else None,
            ))
        result.append((form.get("method", "get").lower(), form.get("action"), tuple(controls)))
    return result


def counterpart_href(english_href: str) -> str:
    if not english_href or english_href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return english_href
    if re.match(r"^[a-z]+://", english_href):
        if english_href.startswith("https://englishire.com/"):
            suffix = english_href.removeprefix("https://englishire.com/")
            if suffix in PAGES or suffix == "":
                return "https://englishire.com/ja/" + suffix
        return english_href
    base, hashmark, fragment = english_href.partition("#")
    query = ""
    if "?" in base:
        base, query = base.split("?", 1)
        query = "?" + query
    if not base:
        return english_href
    filename = Path(base).name
    if filename in PAGES:
        target = filename
    elif filename.endswith((".html", ".htm")):
        target = "../" + base.lstrip("./")
    else:
        target = "../" + base.lstrip("./")
    return target + query + (("#" + fragment) if hashmark else "")


def check_links(en: BeautifulSoup, ja: BeautifulSoup, name: str) -> list[str]:
    errors = []
    en_links = en.find_all("a", href=True)
    ja_links = ja.find_all("a", href=True)
    if len(en_links) != len(ja_links):
        return [f"{name}: anchor count differs ({len(en_links)} vs {len(ja_links)})"]
    for index, (source, target) in enumerate(zip(en_links, ja_links), start=1):
        expected = counterpart_href(str(source["href"]))
        actual = str(target["href"])
        if expected != actual:
            errors.append(f"{name}: link {index} maps to {actual!r}; expected {expected!r}")
    return errors


def check_technical_meta(en: BeautifulSoup, ja: BeautifulSoup, name: str) -> list[str]:
    errors = []
    for attr, key in TECHNICAL_META:
        source = en.find("meta", attrs={attr: key})
        target = ja.find("meta", attrs={attr: key})
        if bool(source) != bool(target):
            errors.append(f"{name}: technical meta {key} presence differs")
        elif source and target and source.get("content") != target.get("content"):
            errors.append(f"{name}: technical meta {key} was translated or changed")
    return errors


def check_pair(name: str) -> list[str]:
    errors = []
    en_path = ROOT / name
    ja_path = ROOT / "ja" / name
    if not ja_path.exists():
        return [f"{name}: missing ja/{name}"]
    try:
        en, ja = parse(en_path), parse(ja_path)
    except ValueError as exc:
        return [str(exc)]

    if ja.html is None or ja.html.get("lang") != "ja":
        errors.append(f"{name}: Japanese html lang is not ja")
    if normalised_body_tokens(en) != normalised_body_tokens(ja):
        errors.append(f"{name}: body DOM, classes, IDs or form semantics differ")
    if section_signature(en) != section_signature(ja):
        errors.append(f"{name}: section/article/aside sequence differs")
    if asset_names(en) != asset_names(ja):
        errors.append(f"{name}: images, stylesheets, scripts, icons or manifests differ")
    if form_signature(en) != form_signature(ja):
        errors.append(f"{name}: form controls, actions or technical values differ")

    en_ids = Counter(tag.get("id") for tag in en.find_all(id=True))
    ja_ids = Counter(tag.get("id") for tag in ja.find_all(id=True))
    if en_ids != ja_ids:
        errors.append(f"{name}: element IDs differ")

    errors.extend(check_links(en, ja, name))
    errors.extend(check_technical_meta(en, ja, name))

    visible = " ".join(
        str(node).strip() for node in ja.find_all(string=True)
        if node.parent and node.parent.name not in {"script", "style", "code", "pre"}
    )
    for bad, preferred in BANNED_TERMS.items():
        if bad in visible:
            errors.append(f"{name}: banned mistranslation {bad!r}; use {preferred!r}")

    words = re.findall(r"\b[A-Za-z]{4,}\b", visible)
    allowed = {
        "Englishire", "Journal", "Tokyo", "Formspree", "Cookie", "WCAG",
        "Email", "English", "Google", "LinkedIn", "Instagram", "YouTube",
    }
    unexplained = [word for word in words if word not in allowed]
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

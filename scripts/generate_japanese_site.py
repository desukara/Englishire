#!/usr/bin/env python3
"""Generate structurally identical Japanese pages from canonical English pages.

The English files remain the source of truth for HTML, CSS classes, images, forms,
inline styles, scripts and page-specific components. Only human-readable text,
metadata, language attributes and internal routes are localised.
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path
from typing import Iterable

from bs4 import BeautifulSoup, Comment, NavigableString
from deep_translator import GoogleTranslator

ROOT = Path(__file__).resolve().parents[1]
JA_DIR = ROOT / "ja"
CACHE_PATH = ROOT / "scripts" / "ja_translation_cache.json"

PAGES = [
    "index.html",
    "teacher-cover.html",
    "how-it-works.html",
    "englishire-standard.html",
    "questions.html",
    "contact.html",
    "about.html",
    "service-standards.html",
    "privacy.html",
    "cookies.html",
    "terms.html",
    "accessibility.html",
    "editorial-policy.html",
    "permissions.html",
    "thank-you.html",
]

# Journal and article pages remain English-only. Links intentionally point outside /ja/.
ENGLISH_ONLY = {
    "journal.html",
    "backup-teacher-eikaiwa.html",
    "easy-teacher.html",
    "eikaiwa-school-operations.html",
    "emergency-classroom-coverage.html",
    "hiring-foreign-teachers-in-japan.html",
    "how-schools-can-handle-staff-shortages.html",
    "real-cost-of-english-teacher-turnover.html",
    "school-collapse-after-three-decades.html",
}

FIXED = {
    "Skip to main content": "本文へ移動",
    "Menu": "メニュー",
    "Teacher Cover": "講師手配",
    "When We Help": "対応できるケース",
    "How It Works": "ご利用の流れ",
    "Journal": "Journal",
    "About": "Englishireについて",
    "Questions": "よくあるご質問",
    "Contact": "お問い合わせ",
    "Request Teacher Cover": "講師手配を相談する",
    "Request a Teacher": "講師手配を相談する",
    "Privacy": "プライバシー",
    "Terms": "利用規約",
    "Cookies": "Cookie",
    "Accessibility": "アクセシビリティ",
    "Editorial Policy": "編集方針",
    "Permissions": "転載・利用許可",
    "Service Standards": "サービス方針",
    "All rights reserved.": "無断転載を禁じます。",
    "Enquiries": "お問い合わせ",
    "Englishire": "Englishire",
    "Englishire Journal": "Englishire Journal",
    "Tokyo": "東京",
    "Temporary Teacher Cover · Tokyo": "東京都内の学校向け英語講師の代講・短期手配",
}

GLOSSARY_REPLACEMENTS = [
    ("代替教師", "代講講師"),
    ("臨時教師", "短期講師"),
    ("教師カバー", "講師の代講"),
    ("教師のカバー", "講師の代講"),
    ("カバー教師", "代講講師"),
    ("生徒", "学習者"),
    ("仕事を見つけるまで", "学校が新しい講師を採用するまで"),
    ("新しい仕事を見つけるまで", "学校が新しい講師を採用するまで"),
    ("英語IRE", "Englishire"),
]

TRANSLATABLE_ATTRS = ("title", "aria-label", "alt", "placeholder", "value")
SKIP_TAGS = {"script", "style", "code", "pre", "svg", "path"}


def load_cache() -> dict[str, str]:
    if CACHE_PATH.exists():
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    return {}


def save_cache(cache: dict[str, str]) -> None:
    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def should_translate(text: str) -> bool:
    stripped = text.strip()
    if not stripped or stripped in FIXED:
        return False
    if re.fullmatch(r"[\d\s\W_]+", stripped):
        return False
    if stripped.startswith(("http://", "https://", "mailto:")):
        return False
    if re.fullmatch(r"[A-Z0-9_.@+\-/]+", stripped) and " " not in stripped:
        return False
    return bool(re.search(r"[A-Za-z]", stripped))


def normalise(text: str) -> str:
    return " ".join(text.split())


def collect_strings(soups: Iterable[BeautifulSoup]) -> list[str]:
    strings: set[str] = set()
    for soup in soups:
        for node in soup.find_all(string=True):
            if isinstance(node, Comment) or (node.parent and node.parent.name in SKIP_TAGS):
                continue
            value = normalise(str(node))
            if should_translate(value):
                strings.add(value)
        for tag in soup.find_all(True):
            for attr in TRANSLATABLE_ATTRS:
                if tag.has_attr(attr):
                    value = normalise(str(tag.get(attr, "")))
                    if should_translate(value):
                        strings.add(value)
        for meta in soup.select('meta[name="description"], meta[property^="og:"], meta[name^="twitter:"]'):
            value = normalise(str(meta.get("content", "")))
            if should_translate(value):
                strings.add(value)
    return sorted(strings)


def translate_all(strings: list[str], cache: dict[str, str]) -> None:
    pending = [s for s in strings if s not in cache and s not in FIXED]
    translator = GoogleTranslator(source="en", target="ja")
    for index in range(0, len(pending), 40):
        batch = pending[index:index + 40]
        translated = None
        for attempt in range(5):
            try:
                translated = translator.translate_batch(batch)
                if translated and len(translated) == len(batch):
                    break
            except Exception as exc:  # network service may throttle temporarily
                print(f"translation retry {attempt + 1}: {exc}", file=sys.stderr)
            time.sleep(2 + attempt * 2)
        if not translated or len(translated) != len(batch):
            raise RuntimeError(f"Translation failed for batch beginning: {batch[0]!r}")
        for source, target in zip(batch, translated):
            cache[source] = target
        save_cache(cache)
        print(f"translated {min(index + len(batch), len(pending))}/{len(pending)}")


def ja_text(source: str, cache: dict[str, str]) -> str:
    value = FIXED.get(source, cache.get(source, source))
    for old, new in GLOSSARY_REPLACEMENTS:
        value = value.replace(old, new)
    return value


def localise_url(url: str, page_name: str) -> str:
    if not url or url.startswith(("#", "mailto:", "tel:", "data:", "javascript:")):
        return url
    if url.startswith("https://englishire.com/"):
        suffix = url.removeprefix("https://englishire.com/")
        if suffix in PAGES or suffix == "":
            return "https://englishire.com/ja/" + suffix
        return url
    if re.match(r"^[a-z]+://", url):
        return url
    base, hashmark, fragment = url.partition("#")
    query = ""
    if "?" in base:
        base, query = base.split("?", 1)
        query = "?" + query
    if not base:
        return url
    filename = Path(base).name
    suffix = Path(base).suffix.lower()
    if filename in PAGES:
        result = filename
    elif filename in ENGLISH_ONLY:
        result = "../" + filename
    elif suffix in {".html", ".htm"}:
        result = "../" + base.lstrip("./")
    else:
        result = "../" + base.lstrip("./")
    return result + query + (("#" + fragment) if hashmark else "")


def localise_json_ld(tag, cache: dict[str, str]) -> None:
    try:
        data = json.loads(tag.string or "")
    except Exception:
        return

    def walk(value):
        if isinstance(value, dict):
            return {key: walk(item) for key, item in value.items()}
        if isinstance(value, list):
            return [walk(item) for item in value]
        if isinstance(value, str):
            if value.startswith("https://englishire.com/"):
                suffix = value.removeprefix("https://englishire.com/")
                if suffix in PAGES or suffix == "":
                    return "https://englishire.com/ja/" + suffix
                return value
            if should_translate(value):
                return ja_text(normalise(value), cache)
        return value

    tag.string = json.dumps(walk(data), ensure_ascii=False, indent=2)


def generate_page(page_name: str, cache: dict[str, str]) -> None:
    source_path = ROOT / page_name
    soup = BeautifulSoup(source_path.read_text(encoding="utf-8"), "html.parser")
    soup.html["lang"] = "ja"

    # Canonical and reciprocal language metadata.
    canonical_url = "https://englishire.com/ja/" + ("" if page_name == "index.html" else page_name)
    canonical = soup.find("link", rel="canonical")
    if canonical:
        canonical["href"] = canonical_url
    for old in list(soup.find_all("link", rel="alternate")):
        if old.get("hreflang") in {"en", "ja", "x-default"}:
            old.decompose()
    head = soup.head
    for lang, href in [
        ("en", "https://englishire.com/" + ("" if page_name == "index.html" else page_name)),
        ("ja", canonical_url),
        ("x-default", "https://englishire.com/" + ("" if page_name == "index.html" else page_name)),
    ]:
        link = soup.new_tag("link", rel="alternate", hreflang=lang, href=href)
        head.append(link)

    # Preserve exact dependencies while adjusting paths from /ja/.
    for tag in soup.find_all(["link", "script", "img", "source"]):
        attr = "href" if tag.name == "link" else "src"
        if tag.has_attr(attr):
            value = str(tag[attr])
            if not value.startswith(("http://", "https://", "//", "data:", "#")):
                tag[attr] = localise_url(value, page_name)
    for anchor in soup.find_all("a", href=True):
        anchor["href"] = localise_url(str(anchor["href"]), page_name)
    for form in soup.find_all("form", action=True):
        action = str(form["action"])
        if not action.startswith(("http://", "https://", "mailto:")):
            form["action"] = localise_url(action, page_name)

    # Translate visible text without modifying scripts, CSS or markup.
    for node in list(soup.find_all(string=True)):
        if isinstance(node, Comment) or (node.parent and node.parent.name in SKIP_TAGS):
            continue
        raw = str(node)
        value = normalise(raw)
        if not value:
            continue
        if value in FIXED or should_translate(value):
            translated = ja_text(value, cache)
            prefix = raw[: len(raw) - len(raw.lstrip())]
            suffix = raw[len(raw.rstrip()):]
            node.replace_with(NavigableString(prefix + translated + suffix))

    for tag in soup.find_all(True):
        for attr in TRANSLATABLE_ATTRS:
            if tag.has_attr(attr):
                value = normalise(str(tag.get(attr, "")))
                if value in FIXED or should_translate(value):
                    tag[attr] = ja_text(value, cache)
    for meta in soup.select('meta[name="description"], meta[property^="og:"], meta[name^="twitter:"]'):
        value = normalise(str(meta.get("content", "")))
        if value in FIXED or should_translate(value):
            meta["content"] = ja_text(value, cache)
    for tag in soup.find_all("script", attrs={"type": "application/ld+json"}):
        localise_json_ld(tag, cache)

    # Ensure Japanese written-correspondence limits remain explicit on service pages.
    if page_name in {"index.html", "teacher-cover.html", "how-it-works.html", "questions.html", "contact.html", "service-standards.html", "terms.html"}:
        main = soup.find("main")
        if main and not soup.select_one(".language-notice--service-boundary"):
            notice = soup.new_tag("aside", attrs={"class": "language-notice language-notice--service-boundary", "aria-label": "言語対応について"})
            strong = soup.new_tag("strong")
            strong.string = "言語対応について"
            notice.append(strong)
            notice.append(" フォームとメールは日本語・英語のどちらでもご利用いただけます。電話、オンライン会議、対面でのやり取りは英語のみです。日本語の書面作成には翻訳ツールを使用する場合があります。")
            first_section = main.find("section")
            if first_section:
                first_section.insert_after(notice)
            else:
                main.insert(0, notice)

    output = "<!DOCTYPE html>\n" + str(soup)
    JA_DIR.mkdir(exist_ok=True)
    (JA_DIR / page_name).write_text(output, encoding="utf-8")


def main() -> None:
    missing = [name for name in PAGES if not (ROOT / name).exists()]
    if missing:
        raise SystemExit(f"Missing canonical pages: {missing}")
    soups = [BeautifulSoup((ROOT / name).read_text(encoding="utf-8"), "html.parser") for name in PAGES]
    cache = load_cache()
    strings = collect_strings(soups)
    translate_all(strings, cache)
    for name in PAGES:
        generate_page(name, cache)
        print(f"generated ja/{name}")
    save_cache(cache)


if __name__ == "__main__":
    main()

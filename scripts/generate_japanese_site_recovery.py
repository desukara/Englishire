#!/usr/bin/env python3
"""Build production Japanese pages from the canonical English HTML.

The English files remain the source of truth for structure, classes, IDs, assets,
forms, inline CSS, scripts and page-specific components. Only visible language,
localised metadata and page-to-page routes change.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup, Doctype

import generate_japanese_site as generator
import generate_japanese_site_fast as fast

CONTEXT_REPLACEMENTS = [
    ("一時的な英語教師の補償", "英語講師の代講・短期手配"),
    ("臨時の英語教師の補償", "英語講師の代講・短期手配"),
    ("臨時英語講師の代講", "英語講師の代講・短期手配"),
    ("英語教師の臨時補償", "英語講師の代講・短期手配"),
    ("英語教師の補償", "英語講師の代講"),
    ("教師の補償", "講師の代講"),
    ("教師カバー", "講師の代講"),
    ("教師のカバー", "講師の代講"),
    ("教師の表紙", "講師手配"),
    ("表紙教師", "代講講師"),
    ("英語教師", "英語講師"),
    ("臨時教師", "短期講師"),
    ("代替教師", "代講講師"),
    ("採用ギャップ", "採用までの空白期間"),
    ("追加需要", "一時的な授業増"),
    ("スケジュールをカバー", "時間割を維持"),
    ("タイムテーブル", "時間割"),
    ("プライマリナビゲーション", "メインナビゲーション"),
    ("英語のホームページ", "Englishireホームページ"),
    ("教師の表紙のアクション", "講師手配ページの操作"),
    ("かなり長い課題", "より長期の業務"),
    ("課題が確認され", "業務が確認され"),
    ("割り当て", "業務"),
    ("仕事を見つけるまで", "学校が新しい講師を採用するまで"),
    ("新しい仕事を見つけるまで", "学校が新しい講師を採用するまで"),
    ("英語IRE", "Englishire"),
    ("|英語", "| Englishire"),
]

EXACT_OVERRIDES = {
    "Temporary English Teacher Cover in Tokyo | Englishire": "東京の学校向け英語講師の代講・短期手配 | Englishire",
    "Temporary English Teacher Cover · Tokyo": "東京都内の学校向け英語講師の代講・短期手配",
    "Cover the timetable without lowering the standard.": "教育の質を保ちながら、時間割の継続を支えます。",
    "Considered temporary English teacher cover for schools facing absence, recruitment gaps, timetable changes and additional demand.": "急な欠勤、採用までの空白期間、時間割の変更、一時的な授業増に対応する、学校向け英語講師の代講・短期手配です。",
    "Englishire exists to preserve the continuity of education whilst schools take the time required to make sound decisions. Whether cover is needed for a single day or a considerably longer assignment, the work begins with a proper understanding of the school, the learners and the lessons concerned.": "Englishireは、学校が採用や運営について十分に検討できる時間を確保しながら、授業の継続を支えるためのサービスです。1日だけの代講でも、より長期の業務でも、まず学校、学習者、授業内容を正確に理解することから始めます。",
    "Primary navigation": "メインナビゲーション",
    "Englishire homepage": "Englishireホームページ",
    "Teacher cover page actions": "講師手配ページの操作",
    "Request Teacher Cover": "講師手配を相談する",
    "When We Help": "対応できるケース",
}

JSON_TRANSLATABLE_KEYS = {
    "name", "description", "serviceType", "headline", "alternativeHeadline",
    "caption", "articleSection", "keywords", "text",
}
JSON_TECHNICAL_KEYS = {
    "@context", "@type", "url", "image", "logo", "sameAs", "email",
    "telephone", "datePublished", "dateModified", "contentUrl",
    "mainEntityOfPage", "inLanguage",
}

original_ja_text = generator.ja_text
original_collect = generator.collect_strings
original_generate_page = generator.generate_page


def polished_ja_text(source: str, cache: dict[str, str]) -> str:
    value = EXACT_OVERRIDES.get(source, original_ja_text(source, cache))
    for old, new in CONTEXT_REPLACEMENTS:
        value = value.replace(old, new)
    return value


def json_strings(value: Any, key: str | None = None):
    if isinstance(value, dict):
        for child_key, child in value.items():
            yield from json_strings(child, child_key)
    elif isinstance(value, list):
        for child in value:
            yield from json_strings(child, key)
    elif isinstance(value, str) and key in JSON_TRANSLATABLE_KEYS and generator.should_translate(value):
        yield generator.normalise(value)


def collect_with_json(soups):
    strings = set(original_collect(soups))
    for soup in soups:
        for tag in soup.find_all("script", attrs={"type": "application/ld+json"}):
            try:
                data = json.loads(tag.string or "")
            except Exception:
                continue
            strings.update(json_strings(data))
    strings.update(EXACT_OVERRIDES)
    return sorted(strings)


def localise_json_ld(tag, cache: dict[str, str]) -> None:
    try:
        data = json.loads(tag.string or "")
    except Exception:
        return

    def walk(value: Any, key: str | None = None):
        if isinstance(value, dict):
            return {child_key: walk(child, child_key) for child_key, child in value.items()}
        if isinstance(value, list):
            return [walk(child, key) for child in value]
        if not isinstance(value, str):
            return value
        if value.startswith("https://englishire.com/"):
            suffix = value.removeprefix("https://englishire.com/")
            if suffix in generator.PAGES or suffix == "":
                return "https://englishire.com/ja/" + suffix
            return value
        if key in JSON_TECHNICAL_KEYS or key is None:
            return value
        if key in JSON_TRANSLATABLE_KEYS and generator.should_translate(value):
            return polished_ja_text(generator.normalise(value), cache)
        return value

    tag.string = json.dumps(walk(data), ensure_ascii=False, indent=2)


def restore_technical_semantics(en: BeautifulSoup, ja: BeautifulSoup) -> None:
    """Restore attributes that must never be translated or reinterpreted."""
    en_tags = en.find_all(True)
    ja_tags = ja.find_all(True)
    if len(en_tags) != len(ja_tags):
        raise RuntimeError("Generated DOM no longer matches canonical English structure")

    for source, target in zip(en_tags, ja_tags):
        for attr in ("name", "type", "method", "enctype", "autocomplete", "min", "max", "step", "pattern", "accept", "multiple", "required"):
            if source.has_attr(attr):
                target[attr] = source[attr]
            elif target.has_attr(attr):
                del target[attr]
        if source.name in {"input", "option"} and source.has_attr("value"):
            input_type = str(source.get("type", "")).lower()
            if source.name == "option" or input_type in {"hidden", "checkbox", "radio", "date", "time", "number", "email"}:
                target["value"] = source["value"]
        for attr in list(target.attrs):
            if attr.startswith("data-") and source.has_attr(attr):
                target[attr] = source[attr]


def postprocess_page(page_name: str, cache: dict[str, str]) -> None:
    path = generator.JA_DIR / page_name
    raw = path.read_text(encoding="utf-8")
    raw = re.sub(r"^<!DOCTYPE html>\s*html\s*", "<!DOCTYPE html>\n", raw, count=1, flags=re.I)
    ja = BeautifulSoup(raw, "html.parser")
    en = BeautifulSoup((generator.ROOT / page_name).read_text(encoding="utf-8"), "html.parser")

    for node in list(ja.contents):
        if isinstance(node, Doctype):
            node.extract()

    # No Japanese-only page sections: translated pages must mirror the English DOM.
    for notice in ja.select(".language-notice--service-boundary"):
        notice.decompose()

    restore_technical_semantics(en, ja)

    canonical_url = "https://englishire.com/ja/" + ("" if page_name == "index.html" else page_name)
    canonical = ja.find("link", rel="canonical")
    if canonical:
        canonical["href"] = canonical_url
    og_url = ja.find("meta", attrs={"property": "og:url"})
    if og_url:
        og_url["content"] = canonical_url

    for selector, attribute in [
        ('meta[property="og:type"]', "content"),
        ('meta[name="twitter:card"]', "content"),
        ('meta[name="robots"]', "content"),
        ('meta[name="msapplication-config"]', "content"),
    ]:
        source = en.select_one(selector)
        target = ja.select_one(selector)
        if source and target and source.has_attr(attribute):
            value = str(source[attribute])
            if selector == 'meta[name="msapplication-config"]' and value and not value.startswith(("http://", "https://", "../")):
                value = "../" + value.lstrip("./")
            target[attribute] = value

    # Preserve technical Schema.org values while localising human-readable fields.
    for tag in ja.find_all("script", attrs={"type": "application/ld+json"}):
        localise_json_ld(tag, cache)

    for node in list(ja.find_all(string=True)):
        if node.parent and node.parent.name in {"script", "style", "code", "pre"}:
            continue
        text = str(node)
        revised = text
        for old, new in CONTEXT_REPLACEMENTS:
            revised = revised.replace(old, new)
        if revised != text:
            node.replace_with(revised)
    for meta in ja.find_all("meta", content=True):
        content = str(meta["content"])
        for old, new in CONTEXT_REPLACEMENTS:
            content = content.replace(old, new)
        meta["content"] = content

    path.write_text("<!DOCTYPE html>\n" + str(ja), encoding="utf-8")


def hardened_generate_page(page_name: str, cache: dict[str, str]) -> None:
    original_generate_page(page_name, cache)
    postprocess_page(page_name, cache)


generator.ja_text = polished_ja_text
generator.collect_strings = collect_with_json
generator.localise_json_ld = localise_json_ld
generator.generate_page = hardened_generate_page
generator.translate_all = fast.parallel_translate_all

if __name__ == "__main__":
    generator.main()

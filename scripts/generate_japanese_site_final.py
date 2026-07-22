#!/usr/bin/env python3
"""Final production runner for Japanese parity recovery."""
from __future__ import annotations

from bs4 import BeautifulSoup

import generate_japanese_site_recovery as recovery

FINAL_REPLACEMENTS = [
    ("info@englishshire.com", "info@englishire.com"),
    ("イングリッシュアイレ", "Englishire"),
    ("イングリッシュアイア", "Englishire"),
    ("英語IRE", "Englishire"),
    ("© 2026 英語です。", "© 2026 Englishire."),
    ("© 2026 英語。", "© 2026 Englishire."),
    ("英語です。無断転載を禁じます。", "Englishire. 無断転載を禁じます。"),
    ("一時的なカバー", "一時的な代講"),
    ("教師のカバー", "講師の代講"),
    ("英語教師", "英語講師"),
    ("教師", "講師"),
    ("先生", "講師"),
    ("時刻表", "時間割"),
    ("公開された標準", "明文化された基準"),
    ("Englishire スタンダード", "Englishireの基準"),
    ("Englishireのスタンダード", "Englishireの基準"),
    ("適切に配置された呼吸室。", "学校が適切な判断をするための時間を確保します。"),
]


def comparable_tags(doc: BeautifulSoup):
    return [
        tag for tag in doc.find_all(True)
        if not (
            tag.name == "link"
            and "alternate" in tag.get("rel", [])
            and tag.get("hreflang") in {"en", "ja", "x-default"}
        )
    ]


def restore_technical_semantics(en: BeautifulSoup, ja: BeautifulSoup) -> None:
    """Restore non-language HTML semantics while allowing hreflang metadata."""
    en_tags = comparable_tags(en)
    ja_tags = comparable_tags(ja)
    if len(en_tags) != len(ja_tags):
        raise RuntimeError(
            f"Generated DOM no longer matches canonical English structure: "
            f"{len(en_tags)} English tags vs {len(ja_tags)} Japanese tags"
        )

    for source, target in zip(en_tags, ja_tags):
        if source.name != target.name:
            raise RuntimeError(
                f"Generated DOM tag mismatch: {source.name!r} vs {target.name!r}"
            )
        for attr in (
            "name", "type", "method", "enctype", "autocomplete", "min", "max",
            "step", "pattern", "accept", "multiple", "required",
        ):
            if source.has_attr(attr):
                target[attr] = source[attr]
            elif target.has_attr(attr):
                del target[attr]
        if source.name in {"input", "option"} and source.has_attr("value"):
            input_type = str(source.get("type", "")).lower()
            if source.name == "option" or input_type in {
                "hidden", "checkbox", "radio", "date", "time", "number", "email"
            }:
                target["value"] = source["value"]
        for attr in list(target.attrs):
            if attr.startswith("data-"):
                if source.has_attr(attr):
                    target[attr] = source[attr]
                else:
                    del target[attr]


original_postprocess = recovery.postprocess_page


def final_postprocess(page_name: str, cache: dict[str, str]) -> None:
    original_postprocess(page_name, cache)
    path = recovery.generator.JA_DIR / page_name
    content = path.read_text(encoding="utf-8")
    for old, new in FINAL_REPLACEMENTS:
        content = content.replace(old, new)
    path.write_text(content, encoding="utf-8")


recovery.restore_technical_semantics = restore_technical_semantics
recovery.postprocess_page = final_postprocess

if __name__ == "__main__":
    recovery.generator.main()

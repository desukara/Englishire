#!/usr/bin/env python3
"""Release runner for fully reviewed Japanese counterparts."""
from __future__ import annotations

import re

from bs4 import BeautifulSoup, NavigableString, Tag

import generate_japanese_site_reviewed as reviewed
from japanese_strict import STRICT_OVERRIDES

# Exact source-keyed translations are the only language source used by the
# release build. The strict coverage audit fails before generation if any
# canonical English string lacks a reviewed Japanese counterpart.
reviewed.final.recovery.EXACT_OVERRIDES.update(STRICT_OVERRIDES)
reviewed.final.recovery.generator.translate_all = lambda strings, cache: None

SERVICE_PAGES = {
    "index.html", "teacher-cover.html", "how-it-works.html",
    "questions.html", "contact.html", "service-standards.html", "terms.html",
}

JAPANESE_CHARACTER = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")
INLINE_CONTAINERS = ("p", "li", "dd", "dt", "figcaption", "span")

original_postprocess = reviewed.final.recovery.postprocess_page


def normalize_japanese_inline_typography(soup: BeautifulSoup) -> None:
    """Remove English punctuation and spacing left around translated inline links."""
    for container in soup.find_all(INLINE_CONTAINERS):
        if not JAPANESE_CHARACTER.search(container.get_text()):
            continue

        for node in list(container.children):
            if not isinstance(node, NavigableString):
                continue

            original = str(node)
            text = original

            if isinstance(node.previous_sibling, Tag):
                text = re.sub(r"^\s*\.\s*", "。", text, count=1)
                text = re.sub(
                    r"^\s+(?=[\u3040-\u30ff\u3400-\u9fff、。])",
                    "",
                    text,
                )

            if isinstance(node.next_sibling, Tag):
                text = re.sub(
                    r"(?<=[\u3040-\u30ff\u3400-\u9fff、。])\s+$",
                    "",
                    text,
                )

            if text != original:
                node.replace_with(text)


def postprocess_with_language_boundary(page_name: str, cache: dict[str, str]) -> None:
    """Generate a parity-safe page, add the language notice, and polish typography."""
    original_postprocess(page_name, cache)

    path = reviewed.final.recovery.generator.JA_DIR / page_name
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")

    if page_name in SERVICE_PAGES:
        for old_notice in soup.select(".language-notice--service-boundary"):
            old_notice.decompose()

        main = soup.find("main")
        if main is None:
            raise RuntimeError(f"{page_name}: no main element for language notice")

        notice = soup.new_tag(
            "aside",
            attrs={
                "class": "language-notice language-notice--service-boundary",
                "aria-label": "言語対応について",
            },
        )
        heading = soup.new_tag("strong")
        heading.string = "言語対応について"
        notice.append(heading)
        notice.append(
            " 日本語でのお問い合わせは、フォームまたはメールで承ります。"
            "電話、オンライン会議、対面での業務上のやり取りは英語で行います。"
            "日本語の文面作成には翻訳支援を使用する場合があります。"
        )

        first_section = main.find("section")
        if first_section is not None:
            first_section.insert_after(notice)
        else:
            main.insert(0, notice)

    normalize_japanese_inline_typography(soup)

    # BeautifulSoup preserves the original document type, so serialise once.
    path.write_text(str(soup), encoding="utf-8")


reviewed.final.recovery.postprocess_page = postprocess_with_language_boundary

if __name__ == "__main__":
    reviewed.final.recovery.generator.main()

#!/usr/bin/env python3
"""Release runner for fully reviewed Japanese counterparts."""
from __future__ import annotations

from bs4 import BeautifulSoup

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

original_postprocess = reviewed.final.recovery.postprocess_page


def postprocess_with_language_boundary(page_name: str, cache: dict[str, str]) -> None:
    """Generate a parity-safe page, then add the required service-language notice."""
    original_postprocess(page_name, cache)
    if page_name not in SERVICE_PAGES:
        return

    path = reviewed.final.recovery.generator.JA_DIR / page_name
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
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

    # BeautifulSoup preserves the original document type, so serialise once.
    path.write_text(str(soup), encoding="utf-8")


reviewed.final.recovery.postprocess_page = postprocess_with_language_boundary

if __name__ == "__main__":
    reviewed.final.recovery.generator.main()

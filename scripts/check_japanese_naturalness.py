#!/usr/bin/env python3
"""Reject wording found during the post-merge natural-Japanese review."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
JA = ROOT / "ja"

BANNED = {
    "長期の短期手配": "数週間以上にわたる一時的な手配",
    "より長い期間の短期手配": "数週間以上にわたる一時的な手配",
    "学校について知らせる": "学校情報を事前に共有する",
    "編集用画像": "記事画像",
    "姿勢は英国らしく": "英国らしい節度を大切にし",
    "特定の近道は使う価値がありません": "品質や安全を損なう近道は選びません",
    "講師に実用的な事前説明を共有": "講師に実用的な事前説明を行う",
    "専門的な自信を持って担当": "落ち着いて責任を果たす",
    "可能な限り高い継続性": "できる限り保たれた授業の流れ",
    "それを尊重して慎重に入るべき": "その文化を尊重して慎重に関わる",
    "ほかの条件は妥当な手配": "ほかの条件に問題のない手配",
    "短期の講師代講": "講師の短期代講",
    "早めのご紹介が役立ちます": "早めの学校情報の共有が役立ちます",
}

errors = []
for path in sorted(JA.glob("*.html")):
    text = path.read_text(encoding="utf-8")
    for bad, preferred in BANNED.items():
        if bad in text:
            errors.append(f"{path.name}: found {bad!r}; prefer {preferred!r}")

if errors:
    print("Japanese naturalness audit failed:", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(f"Japanese naturalness audit passed for {len(list(JA.glob('*.html')))} HTML files.")

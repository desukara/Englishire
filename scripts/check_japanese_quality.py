#!/usr/bin/env python3
"""Fail on known Japanese translation corruptions and protected identifiers."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
JA = ROOT / "ja"

BANNED = {
    "info@englishshire.com": "info@englishire.com",
    "イングリッシュアイレ": "Englishire",
    "イングリッシュアイア": "Englishire",
    "英語IRE": "Englishire",
    "© 2026 英語です。": "© 2026 Englishire.",
    "英語です。無断転載を禁じます。": "Englishire. 無断転載を禁じます。",
    "教師の補償": "講師の代講",
    "英語教師の補償": "英語講師の代講",
    "教師の表紙": "講師手配",
    "講師の表紙": "講師手配",
    "採用ギャップ": "採用までの空白期間",
    "仕事を見つけるまで": "学校が新しい講師を採用するまで",
    "新しい仕事を見つけるまで": "学校が新しい講師を採用するまで",
    "適切に配置された呼吸室": "学校が適切な判断をするための時間",
    "私は": "Englishireは / 当社は",
    "私たちは": "Englishireは / 当社は",
    "私たちの": "Englishireの / 当社の",
    "発売前の適合性": "空き状況より適合性",
    "可用性": "空き状況",
    "ファンファーレ": "目立つ演出",
    "司牧": "学習者支援",
    "旅行の手配": "移動経路・交通手段",
    "無料日記": "予定が空いている",
    "臨時教員": "短期講師",
    "一時的な保護者": "短期講師",
    "調査を確保する": "問い合わせを確保する",
    "時間割のエントリ": "時間割上の人数",
    "日本語学習者": "日本語を母語とする学習者",
    "講師の負担に対する": "講師手配に対する",
}

errors = []
for path in sorted(JA.glob("*.html")):
    text = path.read_text(encoding="utf-8")
    if "info@englishire.com" in text and "mailto:info@englishire.com" not in text:
        errors.append(f"{path.name}: visible contact email is not paired with the correct mailto link")
    for bad, preferred in BANNED.items():
        if bad in text:
            errors.append(f"{path.name}: found {bad!r}; expected {preferred!r}")

if errors:
    print("Japanese quality audit failed:", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(f"Japanese quality audit passed for {len(list(JA.glob('*.html')))} HTML files.")

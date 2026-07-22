#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JA = ROOT / "ja"
REPORT = ROOT / "scripts" / "japanese_quality_report.txt"
BANNED = [
    "info@englishshire.com", "イングリッシュアイレ", "イングリッシュアイア", "英語IRE",
    "教師の補償", "英語教師の補償", "教師の表紙", "講師の表紙", "採用ギャップ",
    "仕事を見つけるまで", "新しい仕事を見つけるまで", "適切に配置された呼吸室",
    "私は", "私たちは", "私たちの", "発売前の適合性", "可用性", "ファンファーレ",
    "司牧", "旅行の手配", "無料日記", "臨時教員", "一時的な保護者",
    "調査を確保する", "時間割のエントリ", "日本語学習者", "講師の負担に対する",
]
lines = []
for path in sorted(JA.glob("*.html")):
    text = path.read_text(encoding="utf-8")
    for phrase in BANNED:
        count = text.count(phrase)
        if count:
            lines.append(f"{path.name}\t{phrase}\t{count}")
REPORT.write_text("\n".join(lines) + ("\n" if lines else "PASS\n"), encoding="utf-8")
print(REPORT.read_text(encoding="utf-8"))

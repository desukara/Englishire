#!/usr/bin/env python3
"""Final release runner for reviewed Japanese counterparts."""

import generate_japanese_site_reviewed as reviewed

reviewed.final.FINAL_REPLACEMENTS.extend([
    ("可用性", "空き状況"),
    ("時間割のエントリ", "時間割上の項目"),
    ("司牧", "学習者支援"),
    ("臨時教員", "短期講師"),
])

if __name__ == "__main__":
    reviewed.final.recovery.generator.main()

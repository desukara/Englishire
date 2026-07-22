#!/usr/bin/env python3
"""Final production runner for Japanese parity recovery."""
from __future__ import annotations

from bs4 import BeautifulSoup

import generate_japanese_site_recovery as recovery
from japanese_editorial_overrides import SOURCE_OVERRIDES

recovery.EXACT_OVERRIDES.update(SOURCE_OVERRIDES)

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
    ("東京市", "東京都内"),
    ("公開された標準", "明文化された基準"),
    ("Englishire スタンダード", "Englishireの基準"),
    ("Englishireのスタンダード", "Englishireの基準"),
    ("適切に配置された呼吸室。", "学校が適切な判断をするための時間を確保します。"),
    ("私は", "Englishireは"),
    ("私たちは", "Englishireは"),
    ("私たちの", "Englishireの"),
    ("私たちが", "Englishireが"),
    ("私たちに", "Englishireに"),
    ("私たちを", "Englishireを"),
    ("責任ある決定を下すほど仕事を理解していません。", "業務内容を十分に理解できない場合、責任ある判断はできません。"),
    ("責任ある判断を下すほど仕事を理解していません。", "業務内容を十分に理解できない場合、責任ある判断はできません。"),
    ("状況を教えてください。直接検討します。", "状況をお知らせください。Englishireが内容を確認し、対応の可否を判断します。"),
    ("教室を再発明するために来たのではありません。教室に奉仕するために来ました。", "既存の授業を作り替えるのではなく、学校が築いてきた授業運営を尊重し、支えることを重視します。"),
    ("教室を再発明するために来たのではなく、教室に奉仕するために来ました。", "既存の授業を作り替えるのではなく、学校が築いてきた授業運営を尊重し、支えることを重視します。"),
    ("調査が確実に行われるようにするためだけに代講を約束しました。", "必要事項を確認し、適切に対応できると判断した場合にのみ、代講を確定します。"),
    ("学習者を時間割の項目として扱う。", "学習者を単なる時間割上の人数として扱わない。"),
    ("学校を紹介してください。", "学校とご依頼内容についてお知らせください。"),
    ("授業は時間割に残ります。それを維持する手助けをしましょう。", "授業を予定どおり継続できるよう支援します。"),
    ("作業は東京とその周辺地域で検討されています。", "東京都内および近隣地域のご依頼を、移動条件を含めて個別に検討します。"),
    ("これは不適切な代替ではありません。", "単に空きを埋めるための代講ではありません。"),
    ("試験、専門プログラム、個人プログラムでは、英語学習の具体的な目的に注意を払う必要があります。", "試験対策、専門コース、個別プログラムでは、英語を学ぶ目的と到達目標を正確に把握する必要があります。"),
    ("日本語学習者を理解する", "日本語を母語とする学習者への理解"),
    ("まったく同じ英語教育方法は一つもありません。", "英語教育の方法は、学校や学習者、目的によって異なります。"),
    ("学校、時間割、学生に関する重要な情報を提供することはできません。", "学校、時間割、学習者に関する重要な情報が不足している場合、適切な手配はできません。"),
    ("旅行や移動を手配する際、時間通りに到着できる信頼性が不十分です。", "移動条件を確認した結果、時間どおりの到着を確実に見込めない場合があります。"),
    ("教育要件が、対応可能な講師の適切な経験の範囲外です。", "授業内容が、対応可能な講師の経験や専門性の範囲を超えている場合があります。"),
    ("提案された期間または条件の範囲内で、お客様の期待に合理的に応えることができません。", "提示された期間や条件では、ご期待に責任を持って応えられない場合があります。"),
    ("仕事を受け入れると、他の確立された責任と仕事自体の基準が損なわれます。", "ご依頼を引き受けることで、既に確定している責任や当該業務の品質を損なうおそれがある場合があります。"),
    ("割り当てを拒否することは、学校に対する判断ではありません。", "ご依頼をお断りすることは、学校を評価するものではありません。"),
    ("便利な保証", "都合のよい確約"),
    ("不健康であることが判明", "後に履行できないことが判明"),
    ("絶対にしてはいけないこと", "行わないこと"),
    ("特定の近道は使う価値がありません。", "品質や安全を損なう近道は選びません。"),
    ("明確な境界線は、贅沢な約束よりも有益です。", "過度な約束より、対応範囲を明確にすることを重視します。"),
    ("すべてのサービスは適合性と可用性に依存します。正常に提供できるかどうかは確認しません。", "すべてのご依頼は、適合性と空き状況を確認したうえで判断します。適切に提供できる見込みを確認せずに確定することはありません。"),
    ("互換性より利便性を優先する", "適合性より利便性を優先する"),
    ("一時的な雇用を不注意な採用として扱う", "短期手配を安易な採用として扱う"),
    ("学校の確立された文化を無視する", "学校が築いてきた方針や文化を軽視する"),
    ("欠勤により時間割が変更される場合があります。学校時間を減らす必要はありません。", "欠勤により時間割の調整が必要になっても、学習時間を安易に減らすべきではありません。"),
    ("講師のカバーを見る", "講師手配について見る"),
    ("学校を変えることはできません。", "学校の方針や運営を勝手に変えることはありません。"),
    ("時間割に気づきました。", "時間割を確認します。"),
    ("まだ説明されていないことに気づきました。", "未共有の事項がないか確認します。"),
    ("学校は、代講講師に時間割で利用できる時間よりもはるかに多くの仕事を割り当てます。", "学校側の準備や付随業務が、時間割上の授業時間を大きく超える場合があります。"),
    (">学校へ<", ">学校に対して<"),
    (">学習者へ<", ">学習者に対して<"),
    (">講師へ<", ">講師に対して<"),
    ("引き受ける前に明確にする必要があります。", "責任を引き受ける前に、必要事項を明確にします。"),
    ("確認する前に明確にする必要があります。", "確定前に必要事項を明確にします。"),
    ("緊急性が不確実性を覆い隠してはなりません。", "急ぎのご依頼であっても、不明点を残したまま確定しません。"),
    ("短期講師は既存の慣行を尊重すべきです。", "短期で担当する講師も、学校の既存方針や授業運営を尊重します。"),
    ("プロフェッショナリズムは一般的に静かです。", "専門性は、落ち着いた準備と着実な対応に表れます。"),
    ("英語のリクエストを断らなければならない場合があります。", "英語講師のご依頼をお断りする場合があります。"),
    ("English ale は何をしますか？", "Englishireはどのようなサービスを提供していますか？"),
    ("重要な情報は利用できません。", "判断に必要な重要情報が不足しています。"),
    ("適切にマッチした講師は無料ではありません。", "空きがあるだけでは、適切な講師とは限りません。"),
    ("可用性だけでは適合性を保証しません。", "空き状況だけで適合性を判断することはできません。"),
    ("旅行は信頼できません。", "移動条件から、確実な到着を見込めない場合があります。"),
    ("通常の状況では、時間厳守の出席が現実的な期待であるべきです。", "通常の条件で、時間どおりの到着を現実的に見込めることが必要です。"),
    ("この仕事にはさまざまな専門知識が必要です。", "この業務には、特定の専門知識や経験が必要です。"),
    ("専門家は、適切で経験豊富な講師を期待しています。", "専門性の高い授業には、適切な経験を持つ講師が必要です。"),
    ("配置の基準が満たされていません。", "手配に必要な基準を満たしていません。"),
    ("緊急だからといって、適切に履行できない約束を誰かに強いるべきではありません。", "急ぎであっても、適切に履行できない約束をするべきではありません。"),
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

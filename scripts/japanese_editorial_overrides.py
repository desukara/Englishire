#!/usr/bin/env python3
"""Human-reviewed Japanese wording for Englishire service and policy copy."""

SOURCE_OVERRIDES = {
    # Teacher Cover: service purpose, decision-making and boundaries.
    "One arrives not to reinvent the classroom, but to serve it.":
        "既存の授業を作り替えるのではなく、学校が築いてきた授業運営を尊重し、支えることを重視します。",
    "An enquiry is not well served by a promise made before the work can be understood. There are occasions when declining an assignment is the more responsible decision.":
        "業務内容を十分に確認する前に確約しても、学校のためにはなりません。責任ある判断として、ご依頼をお断りする場合があります。",
    "Essential information about the school, timetable or learners cannot be provided.":
        "学校、時間割、学習者に関する重要な情報が不足しており、適切な判断ができない場合。",
    "Travel or access arrangements make punctual arrival insufficiently dependable.":
        "移動経路や入館方法を確認した結果、時間どおりの到着を確実に見込めない場合。",
    "The educational demands fall outside the appropriate experience of the available teacher.":
        "授業内容が、対応可能な講師の経験や専門性の範囲を超えている場合。",
    "Expectations cannot reasonably be met within the time or terms proposed.":
        "提示された期間や条件では、ご期待に責任を持って応えられない場合。",
    "Accepting the work would compromise another confirmed responsibility or the standard of the assignment itself.":
        "ご依頼を引き受けることで、既に確定している責任や当該業務の品質を損なうおそれがある場合。",
    "A declined assignment is not a judgement upon the school. It is simply an acknowledgement that confidence is better preserved by honesty than by a convenient assurance which may later prove unsound.":
        "ご依頼をお断りすることは、学校を評価するものではありません。後に履行できないことが判明する都合のよい確約よりも、最初から正直にお伝えする方が信頼を守れるという判断です。",
    "What We Shall Never Do": "Englishireが行わないこと",
    "Certain shortcuts are not worth taking.": "品質や安全を損なう近道は選びません。",
    "A clear boundary is often more useful than an extravagant promise.":
        "過度な約束より、対応できる範囲を明確にすることを重視します。",
    "Promise cover merely to secure an enquiry": "問い合わせを確保するためだけに代講を約束する",
    "Every assignment depends upon suitability and availability. We will not confirm what cannot be delivered properly.":
        "すべてのご依頼は、適合性と空き状況を確認したうえで判断します。適切に提供できない内容を確定することはありません。",
    "Place convenience above suitability": "適合性より利便性を優先する",
    "A teacher's free diary is not, by itself, a sufficient reason to place that person in a particular classroom.":
        "予定が空いているという理由だけで、その講師が特定の授業に適しているとは判断しません。",
    "Treat temporary cover as careless recruitment": "短期の代講手配を安易な採用として扱う",
    "Temporary teaching and permanent recruitment serve different purposes. One should not be misrepresented as the other.":
        "短期の代講と常勤講師の採用は目的が異なります。一方を他方であるかのように扱うことはありません。",
    "Disregard the school's established culture": "学校が築いてきた方針や文化を軽視する",
    "A temporary teacher is there to support the school, not to impose a personal system upon it.":
        "短期で担当する講師は学校を支える立場であり、個人的な方法を押しつける立場ではありません。",
    "Treat pupils as timetable entries": "学習者を単なる時間割上の人数として扱う",
    "Every class contains individuals whose confidence, progress and experience deserve proper consideration.":
        "どのクラスにも、それぞれ異なる自信、学習状況、経験を持つ学習者がいます。一人ひとりに適切な配慮が必要です。",
    "Before the timetable is sent.": "時間割を確定する前に",
    "View teacher cover": "講師手配について見る",
    "The temporary teacher's responsibility is not to arrive with a universal formula. One arrives to understand the environment, to respect what the school has already built and to support it with confidence.":
        "短期で担当する講師の役割は、万能の方法を持ち込むことではありません。学校の環境を理解し、これまで築かれてきた方針や授業運営を尊重したうえで、必要な支援を行います。",

    # About: company voice, responsibilities and principles.
    "We notice the timetable": "Englishireは時間割と移動条件を確認します",
    "We notice the learners": "Englishireは学習者の状況を確認します",
    "We notice the school": "Englishireは学校の方針と運営を確認します",
    "We notice what has not yet been explained": "Englishireは未共有の事項を確認します",
    "Understanding Japanese Learners": "日本語を母語とする学習者への理解",
    "That breadth matters because no universal formula can serve every classroom.":
        "学校、学習者、授業目的が異なれば、適切な英語教育の方法も異なります。",
    "Children, teenagers, adults and specialist learners do not arrive with identical aims or expectations.":
        "子ども、中高生、成人、専門分野の学習者では、英語を学ぶ目的や期待が異なります。",
    "The reason for studying English should influence the manner in which it is taught.":
        "英語を学ぶ目的に応じて、授業方法や重点を調整する必要があります。",
    "Schools entrust temporary teachers with far more than a vacant hour in the timetable.":
        "学校が短期講師に託すものは、時間割上の空いた一コマだけではありません。",
    "To the school": "学校に対して",
    "We owe clear communication, realistic expectations and respect for the organisation's established procedures and culture.":
        "Englishireは、明確な連絡、現実的な見通し、そして学校が築いてきた手順や文化への敬意を大切にします。",
    "To the learner": "学習者に対して",
    "We owe purposeful teaching, calm conduct and recognition that a change of teacher should not make the school day feel careless.":
        "Englishireは、目的のある授業、落ち着いた対応、そして講師が替わっても授業が安易なものにならないことを重視します。",
    "To the teacher": "講師に対して",
    "We owe sufficient information, a proper briefing and an honest account of the assignment before responsibility is accepted.":
        "Englishireは、講師が責任を引き受ける前に、必要な情報、適切な説明、ご依頼内容の正確な提示を行います。",
    "Clarity should precede confirmation": "必要事項を明確にしてから確定する",
    "Dates, times, location, learners, lesson format, materials and expectations should be understood before an assignment is agreed.":
        "ご依頼を確定する前に、日付、時間、場所、学習者、授業形式、教材、ご要望を確認します。",
    "Urgency should not disguise uncertainty": "急ぎであっても不明点を残さない",
    "Where information is incomplete, the uncertainty should be acknowledged rather than concealed beneath a convenient assurance.":
        "情報が不足している場合は、都合のよい確約で曖昧さを隠さず、未確認事項を明確にお伝えします。",
    "A temporary teacher should respect what already exists": "短期で担当する講師も既存の方針を尊重する",
    "The task is to support the school's routines, relationships and educational aims, not to arrive determined to replace them with a personal system.":
        "役割は、学校の運営、関係性、教育目標を支えることです。個人的な方法に置き換えることではありません。",
    "Professionalism is generally quiet": "専門性は、落ち着いた準備と着実な対応に表れる",
    "It is found in punctuality, preparation, sensible communication, confidentiality and composed classroom conduct rather than theatrical promises.":
        "専門性は、大げさな約束ではなく、時間厳守、準備、適切な連絡、守秘義務、落ち着いた授業対応に表れます。",
    "There are occasions when Englishire must decline": "Englishireがご依頼をお断りする場合",
    "An assignment should be declined where it cannot be undertaken suitably, punctually or with the level of preparation the circumstances require.":
        "適切な講師を手配できない場合、時間どおりの到着を見込めない場合、または必要な準備を確保できない場合は、ご依頼をお断りします。",
    "Tell us about the school, its learners and the circumstances in which temporary English teacher cover might prove useful.":
        "学校、学習者、英語講師の代講・短期手配が必要となり得る状況をお知らせください。",
    "Introduce Your School": "学校とご依頼内容を知らせる",

    # Englishire Standard: suitability, preparation, conduct and communication.
    "An assignment should not be accepted before its essential requirements are understood.":
        "必要事項を理解する前に、ご依頼を引き受けるべきではありません。",
    "Urgency is a feature of many staffing enquiries. It is not a reason to dispense with judgement.":
        "講師手配のご相談には緊急性が伴うことがありますが、急ぎであることを理由に必要な判断を省くことはありません。",
    "The fact that a teacher is available does not, by itself, make that teacher suitable.":
        "予定が空いているという理由だけで、その講師が適任とは限りません。",
    "Availability answers only one question. Schools require rather more.":
        "空き状況は判断材料の一つにすぎません。学校には、授業への適合性を含む、より多くの確認が必要です。",
    "Professionalism is most convincing when it is evident in ordinary conduct.":
        "専門性は、日々の落ち着いた行動に表れるときに最も信頼されます。",
    "A temporary teacher is expected to lead the classroom, but not to recast the institution.":
        "短期で担当する講師には授業を進める責任がありますが、学校の方針や運営を作り替える立場ではありません。",
    "Quiet competence is preferable to conspicuous confidence. The purpose of the assignment is to support the school, not to make the temporary teacher its centre of attention.":
        "目立つ自信よりも、落ち着いた実務能力を重視します。ご依頼の目的は学校を支えることであり、短期講師を中心に据えることではありません。",
    "Every school has an established character which temporary cover should seek to understand before it seeks to influence.":
        "どの学校にも、これまで築かれてきた方針や文化があります。短期の代講では、それに影響を与えようとする前に、まず理解することが必要です。",
    "The school remains the principal authority": "学校の方針が基本となります",
    "The temporary teacher contributes professional expertise, but the school determines its policies, routines and educational priorities.":
        "短期講師は専門性を提供しますが、方針、日課、教育上の優先事項を決めるのは学校です。",
    "Good temporary cover should help a school manage the present without losing sight of what follows.":
        "適切な代講は、目の前の授業を支えながら、その後の学校運営にもつながるものであるべきです。",
    "Please include the location, dates, lesson times, learner age groups and the nature of the support required. We will consider the assignment with appropriate care.":
        "場所、日付、授業時間、学習者の年齢層、必要な支援内容をお知らせください。Englishireが内容を丁寧に確認します。",
    "A sensible introduction is preferable to a frantic first conversation.":
        "緊急時の慌ただしい連絡より、事前に学校について共有していただく方が、適切な対応につながります。",
}

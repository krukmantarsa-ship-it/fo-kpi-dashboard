"""
Pre-computed improvement topics for each agent.

ASAT topics: Top 3 lowest-rated topic categories per agent from Snowflake
    Source: ANALYTICS_DB.EMART_CC.CHAT_TOUCH joined with ANALYTICS_DB.DDS_CC.CHAT_ASAT
    Period: 2026-01-01 onwards, minimum 3 rated chats per topic

QA topics: Key focus areas extracted from coaching sessions file
    Source: Copy of Coaching sessions 2026.xlsx (latest available month)
"""

from __future__ import annotations

AGENT_ASAT_TOPICS: dict[str, str] = {
    "Christian Balanay": (
        "- Promos and Cashback Info (avg 2.33, 3 chats)\n"
        "- Card Transaction (avg 2.83, 12 chats)\n"
        "- Account (avg 3.14, 7 chats)"
    ),
    "Maria Christine Dairo": (
        "- Interest Account/Pocket (avg 2.00, 4 chats)\n"
        "- Credit Finmid (avg 2.33, 3 chats)\n"
        "- Feature Request (avg 2.33, 3 chats)"
    ),
    "Ronaldo Galang": (
        "- Credit Finmid (avg 2.25, 4 chats)\n"
        "- Interest Account/Pocket (avg 2.33, 3 chats)\n"
        "- Card Transaction (avg 3.54, 13 chats)"
    ),
    "Leon Dolfus": (
        "- Tariff Plan (avg 2.00, 4 chats)\n"
        "- Account (avg 3.00, 7 chats)\n"
        "- Interest Account/Pocket (avg 3.00, 3 chats)"
    ),
    "Kleoniki Perikleous": (
        "- Team Management (avg 2.33, 3 chats)\n"
        "- Compliance (avg 2.80, 5 chats)\n"
        "- Card (avg 2.86, 7 chats)"
    ),
    "Angelica Langote": (
        "- Treasury (avg 2.33, 3 chats)\n"
        "- Onboarding (avg 2.67, 3 chats)\n"
        "- Promos and Cashback Info (avg 3.00, 4 chats)"
    ),
    "Nicole Anne Abeno": (
        "- Promos and Cashback Info (avg 3.33, 3 chats)\n"
        "- Compliance (avg 3.40, 5 chats)\n"
        "- Interest Account/Pocket (avg 3.50, 4 chats)"
    ),
    "Reginald Ramirez": (
        "- Promos and Cashback Info (avg 3.00, 8 chats)\n"
        "- Card Acquiring (avg 3.33, 3 chats)\n"
        "- Compliance (avg 3.44, 16 chats)"
    ),
    "Anne Luces": (
        "- Team Management (avg 1.33, 3 chats)\n"
        "- Onboarding (avg 2.00, 7 chats)\n"
        "- Account Block/Restriction (avg 2.33, 3 chats)"
    ),
    "Gabriel Alquinto": (
        "- Account Block/Restriction (avg 2.20, 5 chats)\n"
        "- Data Change (avg 3.14, 7 chats)\n"
        "- Team Management (avg 3.40, 5 chats)"
    ),
    "Jessabel Rullan Dulay": (
        "- Account Block/Restriction (avg 1.00, 3 chats)\n"
        "- Treasury (avg 2.00, 3 chats)\n"
        "- Card Acquiring (avg 2.25, 4 chats)"
    ),
    "Katrina Anne Valenzuela": (
        "- Document Request (avg 2.00, 4 chats)\n"
        "- Compliance (avg 2.00, 4 chats)\n"
        "- Account Block/Restriction (avg 2.25, 4 chats)"
    ),
    "Michelle Piquero Tara": (
        "- Account Block/Restriction (avg 2.33, 3 chats)\n"
        "- App (avg 2.33, 3 chats)\n"
        "- Card Transaction (avg 2.42, 12 chats)"
    ),
    "Jeremy James Borreta": (
        "- Interest Account/Pocket (avg 1.67, 6 chats)\n"
        "- Invalid Contact (avg 2.33, 3 chats)\n"
        "- Account Security (avg 2.33, 3 chats)"
    ),
    "Zoe Ymai": (
        "- Interest Account/Pocket (avg 1.00, 4 chats)\n"
        "- Account Block/Restriction (avg 1.25, 4 chats)\n"
        "- Onboarding (avg 1.75, 4 chats)"
    ),
    "Chantika Kartika": (
        "- Credit Finmid (avg 2.50, 4 chats)\n"
        "- Interest Account/Pocket (avg 2.75, 4 chats)\n"
        "- Compliance (avg 2.75, 4 chats)"
    ),
    "Miranti Putri Wardani": (
        "- Onboarding (avg 1.25, 4 chats)\n"
        "- Card Acquiring (avg 1.33, 3 chats)\n"
        "- Compliance (avg 2.29, 7 chats)"
    ),
    "Ricky Adrian Yohanes": "",
    "Eunice Christine Manoe": (
        "- Invalid Contact (avg 1.00, 3 chats)\n"
        "- GDPR Request (avg 1.00, 3 chats)\n"
        "- Interest Account/Pocket (avg 2.50, 4 chats)"
    ),
    "Ruby Ann (RA)": "",
    "Lyca Marie Salarde": (
        "- Compliance (avg 3.29, 7 chats)\n"
        "- Team Management (avg 3.29, 7 chats)\n"
        "- Interest Account/Pocket (avg 3.38, 8 chats)"
    ),
    "Melanie Desembrana": (
        "- Interest Account/Pocket (avg 2.33, 3 chats)\n"
        "- Account (avg 3.00, 7 chats)\n"
        "- Credit Finmid (avg 3.00, 3 chats)"
    ),
    "Lorie Lee Laiño": (
        "- Document Request (avg 2.40, 5 chats)\n"
        "- Interest Account/Pocket (avg 2.56, 9 chats)\n"
        "- Compliance (avg 2.60, 10 chats)"
    ),
    "Kevin Albie Borreta": (
        "- Interest Account/Pocket (avg 2.00, 4 chats)\n"
        "- Account Block/Restriction (avg 2.00, 5 chats)\n"
        "- Invalid Contact (avg 2.33, 3 chats)"
    ),
    "Alvaro Burgos III": (
        "- Tariff Plan (avg 1.33, 3 chats)\n"
        "- Document Request (avg 2.17, 6 chats)\n"
        "- Card Acquiring (avg 2.33, 3 chats)"
    ),
    "Carlo Bahillo": (
        "- Onboarding (avg 2.71, 7 chats)\n"
        "- Interest Account/Pocket (avg 2.92, 13 chats)\n"
        "- Account (avg 3.14, 7 chats)"
    ),
    "Cris John Espanola": (
        "- Account Block/Restriction (avg 2.29, 7 chats)\n"
        "- Interest Account/Pocket (avg 2.71, 7 chats)\n"
        "- Onboarding (avg 3.00, 4 chats)"
    ),
    "Meryll Mecho Belena": (
        "- Compliance (avg 1.00, 4 chats)\n"
        "- Onboarding (avg 2.33, 3 chats)\n"
        "- Transfer (avg 3.17, 30 chats)"
    ),
    "Agy Mustikha Arum": (
        "- Document Request (avg 2.00, 5 chats)\n"
        "- Account Security (avg 2.33, 3 chats)\n"
        "- Data Change (avg 2.75, 4 chats)"
    ),
    "Celine Hartati": (
        "- Compliance (avg 3.00, 3 chats)\n"
        "- Card Transaction (avg 3.39, 18 chats)\n"
        "- Data Change (avg 3.86, 7 chats)"
    ),
    "Airin Anggraini": (
        "- Data Change (avg 2.13, 16 chats)\n"
        "- Account Block/Restriction (avg 3.00, 3 chats)\n"
        "- Card (avg 3.44, 9 chats)"
    ),
    "Amanda Tria Wulandari": (
        "- Data Change (avg 2.60, 10 chats)\n"
        "- App (avg 3.00, 6 chats)\n"
        "- Account (avg 3.14, 7 chats)"
    ),
    "Angelita Abri Berliani": (
        "- Customer Wish Account Closure (avg 1.00, 3 chats)\n"
        "- Compliance (avg 1.89, 9 chats)\n"
        "- App (avg 2.00, 6 chats)"
    ),
    "Crystelle Cabral": (
        "- Invest (avg 1.00, 3 chats)\n"
        "- Crypto (avg 2.00, 4 chats)\n"
        "- Interest Account/Pocket (avg 2.00, 3 chats)"
    ),
    "Dea Legaspi": (
        "- Invest (avg 2.00, 3 chats)\n"
        "- Data Change (avg 2.09, 11 chats)\n"
        "- App (avg 2.60, 5 chats)"
    ),
    "Derek Sebastian": (
        "- Account (avg 1.00, 5 chats)\n"
        "- Invest (avg 1.00, 3 chats)\n"
        "- App (avg 2.00, 3 chats)"
    ),
    "Dhania Permatasari": (
        "- Data Change (avg 1.78, 9 chats)\n"
        "- Promos and Cashback Info (avg 2.00, 4 chats)\n"
        "- App (avg 3.33, 3 chats)"
    ),
    "Guien Stephanie Camposano": (
        "- Data Change (avg 2.15, 13 chats)\n"
        "- Crypto (avg 3.00, 3 chats)\n"
        "- Compliance (avg 3.60, 10 chats)"
    ),
    "Johanes Nathanael Nainggolan": (
        "- Document Request (avg 2.00, 5 chats)\n"
        "- App (avg 2.17, 6 chats)\n"
        "- Data Change (avg 2.28, 29 chats)"
    ),
    "Lyka Jean Boco": (
        "- Promos and Cashback Info (avg 1.50, 4 chats)\n"
        "- Data Change (avg 2.81, 16 chats)\n"
        "- Tariff Plan (avg 3.33, 3 chats)"
    ),
    "Neren Mercedita Adaya": (
        "- Document Request (avg 2.71, 7 chats)\n"
        "- Data Change (avg 3.50, 6 chats)\n"
        "- Compliance (avg 3.50, 14 chats)"
    ),
    "Pamela Figueroa": (
        "- Document Request (avg 2.60, 5 chats)\n"
        "- App (avg 2.75, 4 chats)\n"
        "- Data Change (avg 2.88, 17 chats)"
    ),
    "Queenielyn (Nana) Guinto": (
        "- Compliance (avg 2.00, 4 chats)\n"
        "- Data Change (avg 2.43, 14 chats)\n"
        "- Document Request (avg 2.50, 4 chats)"
    ),
    "Rameses Maghari": (
        "- Data Change (avg 1.40, 10 chats)\n"
        "- App (avg 3.00, 5 chats)\n"
        "- Account (avg 3.00, 3 chats)"
    ),
}


AGENT_QA_TOPICS: dict[str, str] = {
    "Alvaro Burgos III": (
        "- Ensure consistent FCR and avoid response time abuse\n"
        "- Provide accurate customer guidance and clear education\n"
        "- Verify all required documents and include critical info in notes"
    ),
    "Carlo Bahillo": (
        "- Ensure correct problem type, tagging, and note linking\n"
        "- Achieve FCR by confirming transaction details and providing complete education\n"
        "- Follow correct chat workflow and maintain response time standards"
    ),
    "Chantika Kartika": (
        "- Accuracy of information and correct procedure\n"
        "- Investigation and history review\n"
        "- Proper problem type and note\n"
        "- Case ownership and attention to detail"
    ),
    "Cris John Espanola": (
        "- Maintain response time standards (5-minute SLA)\n"
        "- Ensure FCR and provide complete customer education\n"
        "- Follow correct chat workflow and avoid procedural errors in transfers"
    ),
    "Eunice Christine Manoe": (
        "- Ensure FCR by addressing customer requests directly\n"
        "- Follow correct chat workflow including hard close and problem closure\n"
        "- Include all relevant tags and provide complete instructions"
    ),
    "Kevin Albie Borreta": (
        "- Ensure FCR by investigating thoroughly and addressing all concerns\n"
        "- Follow correct chat workflow including timely closes\n"
        "- Include all relevant tags and verify problem types"
    ),
    "Lorie Lee Laiño": (
        "- Tool compliance: attach correct Guru card and use decision tree\n"
        "- Chat workflow: avoid hard closure for unresolved issues\n"
        "- Initial discovery: fully understand concern at the start"
    ),
    "Lyca Marie Salarde": (
        "- SLA adherence: avoid RTA, follow 30-second greeting and thread closure\n"
        "- Tool compliance: edit AI-generated notes, correct Guru cards and problem type\n"
        "- Chat workflow: proper use of hard and soft closure\n"
        "- Adhere to AFC SLA and avoid premature AFC alerts"
    ),
    "Melanie Desembrana": (
        "- SLA adherence: avoid RTA, follow 5-min response time\n"
        "- Incorrect SLA provided for transfers\n"
        "- Tool compliance: close Problem after resolving, use decision tree guru\n"
        "- Investigation gaps: check timeline for rejection reasons"
    ),
    "Meryll Mecho Belena": (
        "- SLA adherence: avoid RTA, follow 5-min response and thread closure\n"
        "- Revisit card re-issuance process and express shipping\n"
        "- Investigation gaps: check VRM before alerting AFC\n"
        "- Tool compliance: correct Problem type and Guru card"
    ),
    "Miranti Putri Wardani": (
        "- SLA adherence: avoid RTA\n"
        "- Chat workflow: avoid hard-closing unresolved cases\n"
        "- Failed to identify a Phishing attempt\n"
        "- Investigation gaps: incorrect card delivery dates, not using Timeline filters\n"
        "- Tool compliance: edit AI-generated notes, correct problem type"
    ),
    "Ricky Adrian Yohanes": (
        "- SLA adherence: numerous KOs for delays of 11-21 minutes\n"
        "- Sends closing message but fails to actually close chat for 14-15 min\n"
        "- Tool compliance: incomplete notes, incorrect tags and Guru card\n"
        "- Chat workflow: consistently hard-closes unresolved threads"
    ),
    "Ruby Ann (RA)": (
        "- SLA adherence: multiple KO marks for RTA, replies reaching 30 min\n"
        "- Chat workflow: hard-closure for unsolved issues\n"
        "- Investigation gaps: asks for details already visible in VRM Timeline\n"
        "- FCR: providing general info instead of addressing specific issue\n"
        "- Tool compliance: use decision tree Guru, edit AI-generated notes"
    ),
    "Zoe Ymai": (
        "- Several incorrect information markdowns (transfer SLA, P-konto, low-turnover fee)\n"
        "- Revisit SDD return process and escalation process\n"
        "- Tool compliance: correct Guru card, problem type, and notes\n"
        "- SLA adherence: thread closure timing issues"
    ),
    "Angelica Langote": (
        "- Ensure correct problem type and SLA are selected\n"
        "- Follow chat workflow and close chats promptly\n"
        "- Clarify customer requests and explore upsell opportunities"
    ),
    "Anne Luces": (
        "- Follow chat workflow consistently including hard closes\n"
        "- Ensure correct problem tagging and Guru card linking\n"
        "- Ask strategic questions and provide full troubleshooting"
    ),
    "Gabriel Alquinto": (
        "- Follow chat workflow and maintain 5-minute response times\n"
        "- Ensure correct problem creation, closure, and accurate information\n"
        "- Provide complete customer education and ensure FCR"
    ),
    "Jeremy James Borreta": (
        "- Follow chat workflow including timely greetings and hard closes\n"
        "- Apply correct tags and procedures\n"
        "- Acknowledge customer dissatisfaction and perform retention attempts"
    ),
    "Jessabel Rullan Dulay": (
        "- Follow chat workflow including hard closes for NFAR cases\n"
        "- Achieve FCR by clarifying inquiries and providing complete information\n"
        "- Maintain attention to response times and note completeness"
    ),
    "Katrina Anne Valenzuela": (
        "- Follow chat workflow including hard closes and problem closure\n"
        "- Improve response time, avoid delays (response time abuse noted)\n"
        "- Apply correct procedure, tagging, ownership, and strategic questions"
    ),
    "Kleoniki Perikleous": (
        "- Ensure chat workflow and response times are consistently followed\n"
        "- Link notes to correct problem and create new problems when required\n"
        "- Achieve FCR and retention goals with clear guidance and reassurance"
    ),
    "Michelle Piquero Tara": (
        "- Follow chat workflow including hard closes and problem closure\n"
        "- Maintain response time within SLA, avoid response time abuse\n"
        "- Ensure FCR, history checks, and effective guidance"
    ),
    "Nicole Anne Abeno": (
        "- Maintain response time within SLA and avoid delays\n"
        "- Follow chat workflow including hard closes and linking notes\n"
        "- Achieve FCR and complete guidance, highlight benefits/solutions"
    ),
    "Reginald Ramirez": (
        "- Follow chat workflow including hard closes and SLA mentions\n"
        "- Ensure FCR and ownership with proper history checks\n"
        "- Improve tool compliance: correct tagging, problem creation, procedures"
    ),
    "Airin Anggraini": (
        "- SLA adherence: avoid exceeding 10-minute response threshold\n"
        "- Procedure: block compromised cards, follow Phishing process\n"
        "- Tool compliance: use Saved Replies, correct tags and Guru cards\n"
        "- Investigation: review customer situation before responding"
    ),
    "Agy Mustikha Arum": (
        "- Tool compliance: problem closure and notes\n"
        "- Communication: correct spelling and proper capitalization\n"
        "- SLA adherence: thread closure after inactivity\n"
        "- Ticket creation: raise BO ticket for transfer concerns"
    ),
    "Amanda Tria Wulandari": (
        "- SLA adherence: follow 5-minute response and thread closure\n"
        "- Procedure: follow correct chargeback process, alert AFC for document issues\n"
        "- Investigation: thoroughly investigate before asking customer\n"
        "- Tool compliance: link Guru cards, correct tags, close Problems"
    ),
    "Angelita Abri Berliani": (
        "- Communication & Tone: avoid arguing, prioritize empathy and de-escalation\n"
        "- SLA adherence: follow 5-minute response and thread closure\n"
        "- Investigation: review account history and Charlie logs\n"
        "- Tool compliance: never send raw Guru links to customers"
    ),
    "Celine Hartati": (
        "- Thread closure: hard vs. soft closure\n"
        "- Provide proactive education instead of directing to check emails\n"
        "- Tool compliance: Problem & Guru card\n"
        "- SLA adherence: follow 5-minute inactivity rule"
    ),
    "Crystelle Cabral": (
        "- SLA adherence: follow 5-minute response and thread closure\n"
        "- Tool compliance: comprehensive notes with transaction details\n"
        "- Investigation: check previous chat logs before asking customer\n"
        "- Communication & Empathy: avoid robotic one-liner responses"
    ),
    "Dea Legaspi": (
        "- SLA adherence: follow 5-minute response and thread closure\n"
        "- Procedure: follow exact processes for lost/reissued cards\n"
        "- Investigation: look for clues in initial messages proactively\n"
        "- Tool compliance: comprehensive notes, correct tags and Problems"
    ),
    "Derek Sebastian": (
        "- SLA adherence: strict 5-minute response (Response Time Abuse)\n"
        "- Procedure: immediately secure account before raising chargebacks\n"
        "- Investigation: check VRM timeline and previous history\n"
        "- Tool compliance: edit AI-generated notes, correct tags and Problems"
    ),
    "Dhania Permatasari": (
        "- SLA adherence: follow 30-second greeting and 5-minute response\n"
        "- Investigation: avoid assumptions, investigate specific details\n"
        "- Procedure: advise on Fiktionsbescheinigung uploads, handle chargebacks\n"
        "- Tool compliance: update notes, create correct Problem type"
    ),
    "Guien Stephanie Camposano": (
        "- SLA adherence: follow 5-minute response and thread closure\n"
        "- Procedure: follow Guru processes (card not received, transfers)\n"
        "- Investigation: review previous messages and Charlie logs\n"
        "- Tool compliance: edit AI-generated notes, correct Guru card and tags"
    ),
    "Johanes Nathanael Nainggolan": (
        "- SLA adherence: follow 5-minute response (10-min threshold = auto KO)\n"
        "- Tool compliance: edit AI notes, include merchant name and CB escalation #\n"
        "- Tool compliance: manage Problems, correct Charlie descriptions\n"
        "- Investigation: use VRM before asking customer for information"
    ),
    "Lyka Jean Boco": (
        "- SLA adherence: strict 5-minute response (Response Time Abuse)\n"
        "- Investigation: check account history before asking questions\n"
        "- Clear customer education: address all parts of concern proactively\n"
        "- Procedure: provide accurate timeframes for refunds and card delivery"
    ),
    "Neren Mercedita Adaya": (
        "- SLA adherence: follow 5-minute response and thread closure\n"
        "- Investigation: review Notes, VRM timeline, and Charlie logs\n"
        "- Tool compliance: edit AI notes, include transaction info and Slack links\n"
        "- Thread closure: use soft closure for unconfirmed concerns"
    ),
    "Pamela Figueroa": (
        "- SLA adherence: follow 5-minute response time\n"
        "- Investigation: check Charlie logs before responding\n"
        "- Complete resolution & FCR: address every question before closing\n"
        "- Procedure: follow chargeback decision tree, reissue card immediately"
    ),
    "Queenielyn (Nana) Guinto": (
        "- SLA adherence: strict 5-minute response (Response Time Abuse)\n"
        "- Procedure: follow chargeback processes, gather info before escalating\n"
        "- Complete resolution & FCR: address all parts of inquiry\n"
        "- Investigation: review previous threads and notes before asking"
    ),
    "Rameses Maghari": (
        "- SLA adherence: critical area, strict 5-minute response and closure\n"
        "- Procedure: immediately reissue card for unauthorized transactions\n"
        "- Communication & Empathy: include acknowledgment and empathy statements\n"
        "- Tool compliance: avoid linking notes to old unrelated Problems"
    ),
}


def get_asat_topics(display_name: str) -> str:
    return AGENT_ASAT_TOPICS.get(display_name, "")


def get_qa_topics(display_name: str) -> str:
    return AGENT_QA_TOPICS.get(display_name, "")

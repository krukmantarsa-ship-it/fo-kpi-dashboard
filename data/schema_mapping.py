"""
Schema mapping: ANALYTICS_DB.EMART_CC.CHAT_TOUCH → Front Office KPIs.

This module documents how each KPI maps to Snowflake columns and provides
the SQL templates used to compute metrics. The dashboard can run with
mock data or swap to live Snowflake queries using these mappings.

Related tables:
  - REPORT_DB.CC.EXPERT_ASAT_DETAILS  (ASAT ratings, skill routing, team codes)
  - REPORT_DB.CC.QUEUE_ENTRIES_AGENT   (queue team assignment: FO / SME)
"""

# ─── Filter predicates ────────────────────────────────────────────────
AGENT_HANDLER_FILTER = "TOUCH_HANDLER_CD IN ('AGENT', 'AGENT+CHATBOT')"
CHANNEL_CHAT = "TOUCH_COMMUNICATION_CHANNEL_CD = 'CHAT'"
CHANNEL_EMAIL = "TOUCH_COMMUNICATION_CHANNEL_CD = 'EMAIL'"
CHANNEL_BOTH = "TOUCH_COMMUNICATION_CHANNEL_CD IN ('CHAT', 'EMAIL')"

# ─── KPI → Snowflake column mapping ──────────────────────────────────
KPI_COLUMN_MAP = {
    "FRT": {
        "description": "First Response Time (minutes)",
        "source_table": "ANALYTICS_DB.EMART_CC.CHAT_TOUCH",
        "column": "TOUCH_AGENT_FR_IN_TOUCH_DU_IN_MIN",
        "aggregation": "AVG",
        "unit": "min",
        "notes": (
            "Average of TOUCH_AGENT_FR_IN_TOUCH_DU_IN_MIN per agent. "
            "Only for touches where handler is AGENT or AGENT+CHATBOT. "
            "Alternative: DATEDIFF(min, TOUCH_FIRST_CUSTOMER_MESSAGE_AT, "
            "TOUCH_FIRST_AGENT_MESSAGE_AT)."
        ),
    },
    "AHT": {
        "description": "Average Handle Time (minutes)",
        "source_table": "ANALYTICS_DB.EMART_CC.CHAT_TOUCH",
        "column": "TOUCH_AGENT_HANDLING_DU_IN_MIN",
        "aggregation": "AVG",
        "unit": "min",
        "notes": "Average of TOUCH_AGENT_HANDLING_DU_IN_MIN per agent.",
    },
    "Volume": {
        "description": "Total touches handled",
        "source_table": "ANALYTICS_DB.EMART_CC.CHAT_TOUCH",
        "column": "TOUCH_HK",
        "aggregation": "COUNT",
        "unit": "touches",
        "notes": (
            "COUNT of TOUCH_HK WHERE TOUCH_HANDLER_CD IN ('AGENT','AGENT+CHATBOT') "
            "AND TOUCH_END_SUPER_TYPE_CD = 'CLOSED'."
        ),
    },
    "CPH": {
        "description": "Closed Chats & Emails Per Hour",
        "source_table": "ANALYTICS_DB.EMART_CC.CHAT_TOUCH",
        "column": "derived",
        "aggregation": "derived",
        "unit": "per hour",
        "notes": (
            "Volume of CLOSED touches / estimated work hours. "
            "Work hours derived from active touch time range per agent per day, "
            "or configurable hourly assumption (default 8h/day). "
            "Tableau source: 'CPH (All Closed Chats & Emails Per Hour)'."
        ),
    },
    "ASAT": {
        "description": "Agent Satisfaction (1–5 scale)",
        "source_table": "REPORT_DB.CC.EXPERT_ASAT_DETAILS",
        "column": "CHAT_ASAT_RATING_NUM",
        "aggregation": "AVG",
        "unit": "rating (1-5)",
        "join": "JOIN via CHAT_HK or TOUCH_AGENT_HK",
        "notes": (
            "Average of CHAT_ASAT_RATING_NUM from EXPERT_ASAT_DETAILS. "
            "Scale 1–5. Joined to CHAT_TOUCH via CHAT_HK."
        ),
    },
    "QA": {
        "description": "Quality Assurance score",
        "source_table": "MANUAL (Coaching File)",
        "column": "N/A – manual entry",
        "aggregation": "N/A",
        "unit": "0–1 (percentage)",
        "notes": (
            "From 'Copy of Coaching sessions 2026.xlsx'. "
            "Monthly QA scores per agent (0–1 scale). "
            "Editable in dashboard. No Snowflake source."
        ),
    },
}

# ─── SQL templates ────────────────────────────────────────────────────
SQL_AGENT_KPI = """
SELECT
    TOUCH_AGENT_FULL_NAME_NM                          AS agent_name,
    COUNT(*)                                           AS volume,
    AVG(TOUCH_AGENT_FR_IN_TOUCH_DU_IN_MIN)            AS avg_frt_min,
    AVG(TOUCH_AGENT_HANDLING_DU_IN_MIN)                AS avg_aht_min,
    COUNT(*) / NULLIF(
        DATEDIFF('hour',
            MIN(TOUCH_START_AT),
            MAX(TOUCH_END_AT)
        ), 0)                                          AS cph_estimate
FROM ANALYTICS_DB.EMART_CC.CHAT_TOUCH
WHERE {handler_filter}
  AND {channel_filter}
  AND TOUCH_END_SUPER_TYPE_CD = 'CLOSED'
  AND TOUCH_START_AT BETWEEN '{start_date}' AND '{end_date}'
  AND TOUCH_AGENT_FULL_NAME_NM IN ({agent_names})
GROUP BY TOUCH_AGENT_FULL_NAME_NM
"""

SQL_ASAT = """
SELECT
    a.AGENT_FULL_NAME_NM                              AS agent_name,
    AVG(a.CHAT_ASAT_RATING_NUM)                       AS avg_asat
FROM REPORT_DB.CC.EXPERT_ASAT_DETAILS a
WHERE a.DAY_DT BETWEEN '{start_date}' AND '{end_date}'
  AND a.CHAT_ASAT_RATING_NUM IS NOT NULL
  AND a.AGENT_FULL_NAME_NM IN ({agent_names})
GROUP BY a.AGENT_FULL_NAME_NM
"""

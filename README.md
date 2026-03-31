# Front Office KPI Dashboard

Interactive dashboard for Front Office team performance scoring, ranking, and analysis.

## Quick Start

```bash
cd fo-kpi-dashboard
uv venv .local
source .local/bin/activate
uv pip install -r requirements.txt
streamlit run app.py
```

## Teams

| Team | Sub-team | Agents |
|------|----------|--------|
| SME | Veru (14 agents) | Christian Balanay, Maria Christine Dairo, Ronaldo Galang, Leon Dolfus, Kleoniki Perikleous, Angelica Langote, Nicole Anne Abeno, Reginald Ramirez, Anne Luces, Gabriel Alquinto, Jessabel Rullan Dulay, Katrina Anne Valenzuela, Michelle Piquero Tara, Jeremy James Borreta |
| SME | Adhi (16 agents) | Zoe Ymai, Chantika Kartika, Miranti Putri Wardani, Ricky Adrian Yohanes, Eunice Christine Manoe, Ruby Ann, Lyca Marie Salarde, Melanie Desembrana, Lorie Lee Laiño, Kevin Albie Borreta, Alvaro Burgos III, Carlo Bahillo, Cris John Espanola, Meryll Mecho Belena, Agy Mustikha Arum, Celine Hartati |
| Retail (FO) | — (14 agents) | Airin Anggraini, Amanda Tria Wulandari, Angelita Abri Berliani, Crystelle Cabral, Dea Legaspi, Derek Sebastian, Dhania Permatasari, Guien Stephanie Camposano, Johanes Nathanael Nainggolan, Lyka Jean Boco, Neren Mercedita Adaya, Pamela Figueroa, Queenielyn Guinto, Rameses Maghari |

## KPI Definitions

| KPI | Formula | Source | Unit |
|-----|---------|--------|------|
| **FRT** | AVG(TOUCH_AGENT_FR_IN_TOUCH_DU_IN_MIN) | CHAT_TOUCH | minutes |
| **AHT** | AVG(TOUCH_AGENT_HANDLING_DU_IN_MIN) | CHAT_TOUCH | minutes |
| **Volume** | COUNT(touches) WHERE handler IN (AGENT, AGENT+CHATBOT) AND closed | CHAT_TOUCH | count |
| **CPH** | Closed volume / work hours | CHAT_TOUCH (derived) | per hour |
| **ASAT** | AVG(CHAT_ASAT_RATING_NUM) | EXPERT_ASAT_DETAILS | 1–5 |
| **QA** | Manual score from coaching file | Coaching Sessions xlsx | 0–1 |

## Scoring

- Max score = 100%
- KPI weights are configurable via sidebar sliders
- Default weights: CPH 30%, ASAT 30%, QA 20%, FRT 10%, AHT 10%
- Volume is informational (weight 0% by default)
- Lower-is-better KPIs (FRT, AHT) use inverse normalisation
- Higher-is-better KPIs (CPH, ASAT, QA) use direct normalisation

## Schema Mapping: ANALYTICS_DB.EMART_CC.CHAT_TOUCH

### Fields used for KPIs

| Snowflake Column | KPI | Notes |
|-----------------|-----|-------|
| TOUCH_AGENT_FR_IN_TOUCH_DU_IN_MIN | FRT | Agent first response time within touch (minutes) |
| TOUCH_AGENT_HANDLING_DU_IN_MIN | AHT | Agent handling duration (minutes) |
| TOUCH_HK (COUNT) | Volume | Count of closed touches per agent |
| TOUCH_HANDLER_CD | Filter | IN ('AGENT', 'AGENT+CHATBOT') |
| TOUCH_END_SUPER_TYPE_CD | Filter | = 'CLOSED' for volume/CPH |
| TOUCH_COMMUNICATION_CHANNEL_CD | Filter | 'CHAT' or 'EMAIL' |
| TOUCH_AGENT_FULL_NAME_NM | Agent ID | Matched to team mapping |
| TOUCH_START_AT / TOUCH_END_AT | Period | Date range filtering |

### Related tables

| Table | Purpose | Join Key |
|-------|---------|----------|
| REPORT_DB.CC.EXPERT_ASAT_DETAILS | ASAT ratings, skills | CHAT_HK or TOUCH_AGENT_HK |
| REPORT_DB.CC.QUEUE_ENTRIES_AGENT | Queue team (FO/SME) | CHAT_HK |

## Data Layer

Currently uses **mock data** calibrated from real Snowflake patterns. To switch to live data:

1. Add `snowflake-connector-python` to requirements.txt
2. Implement query functions in `data/schema_mapping.py` using the SQL templates
3. Replace `generate_agent_data()` calls with live query results

## Missing Data / Open Questions

| Item | Status | Notes |
|------|--------|-------|
| QA scores | Manual | From coaching file, not in Snowflake |
| Adherence | Skipped | No source identified; excluded from scoring |
| CPH work hours | Estimated | No shift/schedule table; derived from activity range |
| Agent-team mapping | Hardcoded | No Snowflake field for Veru/Adhi split |

## Project Structure

```
fo-kpi-dashboard/
├── app.py                      # Main Streamlit dashboard
├── data/
│   ├── agent_mapping.py        # Agent → team mapping
│   ├── schema_mapping.py       # Snowflake column mapping + SQL templates
│   ├── scoring.py              # Scoring engine (normalisation, weighting)
│   └── mock_data.py            # Mock data generator
├── components/
│   ├── filters.py              # Sidebar filters
│   ├── kpi_cards.py            # KPI summary cards
│   ├── agent_table.py          # Ranking table + agent detail
│   └── charts.py               # Plotly chart components
├── .streamlit/config.toml      # Dark theme config
├── requirements.txt
└── README.md
```

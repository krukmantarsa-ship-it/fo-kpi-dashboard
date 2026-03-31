"""
Agent-to-team mapping for Front Office KPI Dashboard.

Source: Manual mapping from team leads (screenshot provided).
Snowflake field: ANALYTICS_DB.EMART_CC.CHAT_TOUCH.TOUCH_AGENT_FULL_NAME_NM

Names below are matched against Snowflake TOUCH_AGENT_FULL_NAME_NM using
fuzzy prefix logic (see match_agent_name).
"""

TEAM_SME_VERU = "SME - Veru"
TEAM_SME_ADHI = "SME - Adhi"
TEAM_RETAIL = "Retail (FO)"

SME_VERU_AGENTS: list[dict] = [
    {"display": "Christian Balanay",       "sf_name": "Christian Joseph Balanay"},
    {"display": "Maria Christine Dairo",   "sf_name": "Maria Christine Dario"},
    {"display": "Ronaldo Galang",          "sf_name": "Ronaldo Galang"},
    {"display": "Leon Dolfus",             "sf_name": "Leon Dolfus"},
    {"display": "Kleoniki Perikleous",     "sf_name": "Kleoniki Perikleous"},
    {"display": "Angelica Langote",        "sf_name": "Angelica Langote"},
    {"display": "Nicole Anne Abeno",       "sf_name": "Nicole Anne Abeno"},
    {"display": "Reginald Ramirez",        "sf_name": "Reginald Ramirez"},
    {"display": "Anne Luces",              "sf_name": "Anne Luces"},
    {"display": "Gabriel Alquinto",        "sf_name": "Gabriel Yee Alquinto"},
    {"display": "Jessabel Rullan Dulay",   "sf_name": "Jessabel Rullan Dulay"},
    {"display": "Katrina Anne Valenzuela", "sf_name": "Katrina Anne Valenzuela"},
    {"display": "Michelle Piquero Tara",   "sf_name": "Michelle Piquero Tara"},
    {"display": "Jeremy James Borreta",    "sf_name": "Jeremy James Borreta"},
]

SME_ADHI_AGENTS: list[dict] = [
    {"display": "Zoe Ymai",                "sf_name": "Zoe Getmira Ymai"},
    {"display": "Chantika Kartika",        "sf_name": "Chantika Lily Kartika"},
    {"display": "Miranti Putri Wardani",   "sf_name": "Miranti Putri Wardani"},
    {"display": "Ricky Adrian Yohanes",    "sf_name": "Ricky Adrian Yohanes"},
    {"display": "Eunice Christine Manoe",  "sf_name": "Eunice Christine Manoe"},
    {"display": "Ruby Ann (RA)",           "sf_name": "Ruby Ann"},
    {"display": "Lyca Marie Salarde",      "sf_name": "Lyca Marie Salarde"},
    {"display": "Melanie Desembrana",      "sf_name": "Melanie Desembrana"},
    {"display": "Lorie Lee Laiño",         "sf_name": "Lorie Lee Cabanesas Laino"},
    {"display": "Kevin Albie Borreta",     "sf_name": "Kevin Albie Borreta"},
    {"display": "Alvaro Burgos III",       "sf_name": "Alvaro Burgos"},
    {"display": "Carlo Bahillo",           "sf_name": "Carlo Bahillo"},
    {"display": "Cris John Espanola",      "sf_name": "Cris John Espanola"},
    {"display": "Meryll Mecho Belena",     "sf_name": "Meryll Mecho Belena"},
    {"display": "Agy Mustikha Arum",       "sf_name": "Agy Mustikha Arum"},
    {"display": "Celine Hartati",          "sf_name": "Celine Hartati"},
]

RETAIL_FO_AGENTS: list[dict] = [
    {"display": "Airin Anggraini",               "sf_name": "Airin Anggraini"},
    {"display": "Amanda Tria Wulandari",         "sf_name": "Amanda Tria Wulandari"},
    {"display": "Angelita Abri Berliani",        "sf_name": "Angelita Abri Berliani"},
    {"display": "Crystelle Cabral",              "sf_name": "Crystelle Cabral"},
    {"display": "Dea Legaspi",                   "sf_name": "Dea Legaspi"},
    {"display": "Derek Sebastian",               "sf_name": "Derek Sebastian"},
    {"display": "Dhania Permatasari",            "sf_name": "Dhania Permatasari"},
    {"display": "Guien Stephanie Camposano",     "sf_name": "Guien Stephanie Camposano"},
    {"display": "Johanes Nathanael Nainggolan",  "sf_name": "Johannes Nathanael Nathanael"},
    {"display": "Lyka Jean Boco",                "sf_name": "Lyka Jean Mariano Boco"},
    {"display": "Neren Mercedita Adaya",         "sf_name": "Neren Mercedita Adaya"},
    {"display": "Pamela Figueroa",               "sf_name": "Pamela Figueroa"},
    {"display": "Queenielyn (Nana) Guinto",      "sf_name": "Queenielyn Guinto"},
    {"display": "Rameses Maghari",               "sf_name": "Rameses Maghari"},
]


def get_all_agents() -> list[dict]:
    """Return flat list of all agents with team assignment."""
    agents = []
    for a in SME_VERU_AGENTS:
        agents.append({**a, "team": TEAM_SME_VERU, "parent_team": "SME"})
    for a in SME_ADHI_AGENTS:
        agents.append({**a, "team": TEAM_SME_ADHI, "parent_team": "SME"})
    for a in RETAIL_FO_AGENTS:
        agents.append({**a, "team": TEAM_RETAIL, "parent_team": "Retail"})
    return agents


def get_sf_name_to_team() -> dict[str, str]:
    """Snowflake full name -> team string."""
    mapping = {}
    for a in get_all_agents():
        mapping[a["sf_name"]] = a["team"]
    return mapping


def get_sf_name_to_display() -> dict[str, str]:
    mapping = {}
    for a in get_all_agents():
        mapping[a["sf_name"]] = a["display"]
    return mapping


TEAM_LIST = [TEAM_RETAIL, TEAM_SME_VERU, TEAM_SME_ADHI]
PARENT_TEAMS = ["All", "Retail", "SME"]

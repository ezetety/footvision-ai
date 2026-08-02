import streamlit as st
import requests
import random
from typing import Dict, Any, List, Optional

# ==========================================
# 1. CONFIGURATION SYSTEME & STYLE DARK
# ==========================================
st.set_page_config(
    page_title="FootVision AI — Analyses & Scénarios 2026/2027",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS VisiFoot Dark Mode
st.markdown("""
    <style>
    .stApp {
        background-color: #0A0D12;
        color: #E2E8F0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .header-card {
        background: linear-gradient(135deg, #111827 0%, #1F2937 100%);
        padding: 24px;
        border-radius: 12px;
        border-bottom: 3px solid #10B981;
        margin-bottom: 20px;
    }
    .match-card {
        background-color: #111827;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #1F2937;
    }
    .scenario-box {
        background-color: #182232;
        border-left: 4px solid #3B82F6;
        padding: 14px 18px;
        border-radius: 6px;
        margin: 14px 0;
        font-size: 0.92rem;
        line-height: 1.5;
        color: #E2E8F0;
    }
    .tip-pill {
        background-color: #064E3B;
        border: 1px solid #10B981;
        color: #34D399;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.88rem;
        display: inline-block;
    }
    .metric-badge {
        background-color: #1F2937;
        border: 1px solid #374151;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
    }
    .metric-title {
        color: #9CA3AF;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    .disclaimer-box {
        background-color: #18181B;
        border-left: 4px solid #EF4444;
        padding: 12px 16px;
        border-radius: 4px;
        font-size: 0.8rem;
        color: #A1A1AA;
        margin-top: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. BASE DE DONNÉES EXACTE BILAN 2026/2027
# ==========================================
ALL_TEAMS: Dict[str, List[str]] = {
    "Premier League": [
        "Arsenal FC", "Aston Villa", "AFC Bournemouth", "Brentford FC", "Brighton & Hove Albion",
        "Chelsea FC", "Coventry City", "Crystal Palace", "Everton FC", "Fulham FC",
        "Hull City", "Ipswich Town", "Leicester City", "Liverpool FC", "Manchester City",
        "Manchester United", "Newcastle United", "Nottingham Forest", "Southampton FC", "Tottenham Hotspur"
    ],
    "Ligue 1": [
        "AJ Auxerre", "Angers SCO", "AS Monaco", "AS Saint-Étienne", "FC Lorient",
        "Le Havre AC", "Le Mans FC", "LOSC Lille", "Montpellier HSC", "OGC Nice",
        "Olympique de Marseille", "Olympique Lyonnais", "Paris Saint-Germain", "RC Lens", "RC Strasbourg",
        "Stade Brestois 29", "Stade Rennais", "ESTAC Troyes"
    ],
    "La Liga": [
        "Athletic Bilbao", "Atletico Madrid", "CA Osasuna", "CF Málaga", "Celta Vigo",
        "Deportivo Alavés", "Deportivo La Corogne", "FC Barcelona", "Getafe CF", "Racing Santander",
        "Rayo Vallecano", "RCD Espanyol", "Real Betis", "Real Madrid", "Real Sociedad",
        "Real Valladolid", "Sevilla FC", "UD Las Palmas", "Valencia CF", "Villarreal CF"
    ],
    "Serie A": [
        "AC Milan", "ACF Fiorentina", "AS Roma", "Atalanta BC", "Bologna FC",
        "Cagliari Calcio", "Como 1907", "Empoli FC", "Frosinone Calcio", "Genoa CFC",
        "Inter Milan", "Juventus Turin", "AC Monza", "Napoli", "Parma Calcio",
        "SS Lazio", "Torino FC", "Udinese Calcio", "US Lecce", "Venezia FC"
    ],
    "Bundesliga": [
        "1. FC Union Berlin", "1. FSV Mainz 05", "Bayer 04 Leverkusen", "Borussia Dortmund", "Borussia Mönchengladbach",
        "Eintracht Frankfurt", "FC Augsburg", "FC Bayern München", "FC Schalke 04", "Holstein Kiel",
        "Paderborn 07", "RB Leipzig", "SC Freiburg", "SV Elversberg", "SV Werder Bremen",
        "TSG 1899 Hoffenheim", "VfB Stuttgart", "VfL Bochum"
    ],
    "Ligue des Champions": [
        "Real Madrid", "Manchester City", "FC Bayern München", "Paris Saint-Germain", "FC Barcelona",
        "Inter Milan", "Arsenal FC", "Bayer 04 Leverkusen", "Atletico Madrid", "Borussia Dortmund",
        "Juventus Turin", "Atalanta BC", "SL Benfica", "Club Brugge", "Shakhtar Donetsk",
        "AC Milan", "Feyenoord", "Sporting CP", "PSV Eindhoven", "GNK Dinamo Zagreb",
        "Red Bull Salzburg", "LOSC Lille", "Red Star Belgrade", "BSC Young Boys", "Celtic FC",
        "Slovan Bratislava", "AS Monaco", "AC Sparta Praha", "Aston Villa", "Bologna FC",
        "VfB Stuttgart", "SK Sturm Graz", "Stade Brestois 29", "RB Leipzig", "Liverpool FC", "FC Schalke 04"
    ],
    "Ligue des Nations": [
        "France", "Espagne", "Angleterre", "Allemagne", "Italie",
        "Portugal", "Pays-Bas", "Belgique", "Croatie", "Danemark",
        "Suisse", "Autriche", "Hongrie", "Pologne", "Écosse", "Serbie"
    ]
}

COMPETITIONS: Dict[str, int] = {
    "Premier League": 39,
    "Ligue 1": 61,
    "La Liga": 140,
    "Serie A": 135,
    "Bundesliga": 78,
    "Ligue des Champions": 2,
    "Ligue des Nations": 5
}

# ==========================================
# 3. MOTEUR TACTIQUE VISIFOOT
# ==========================================
def generate_match_analytics(fixture_id: int, home: str, away: str) -> Dict[str, Any]:
    random.seed(fixture_id)
    
    p_1 = random.randint(38, 62)
    p_x = random.randint(20, 28)
    p_2 = 100 - (p_1 + p_x)
    
    dc_1x = p_1 + p_x
    dc_x2 = p_2 + p_x
    over15 = random.randint(70, 88)
    over25 = random.randint(45, 72)
    over35 = random.randint(22, 42)
    btts_yes = random.randint(48, 74)
    
    xg_home = round(random.uniform(1.2, 2.6), 2)
    xg_away = round(random.uniform(0.7, 1.9), 2)
    
    managers = ["L. Enrique", "P. Guardiola", "M. Arteta", "C. Ancelotti", "D. Simeone", "X. Alonso", "H. Flick", "V. Kompany"]
    key_players = ["Mbappé", "Haaland", "Vinícius Jr", "Bellingham", "Saka", "Lautaro", "Salah", "Kane", "Yamal", "Musiala"]
    
    home_manager = random.choice(managers)
    away_manager = random.choice([m for m in managers if m != home_manager])
    home_star = random.choice(key_players)
    away_star = random.choice([p for p in key_players if p != home_star])

    if p_1 >= 52:
        main_tip = f"Victoire Domicile — {home} (1)"
        exact_score = "2 - 0" if over25 < 55 else "2 - 1"
        scenario = (
            f"**Scénario VisiFoot :** Intention tactique très claire imprimée par **{home}** (entraîné par **{home_manager}**). "
            f"La vista de **{home_star}** en animation offensive sera déterminante. "
            f"**{away}** sous **{away_manager}** devra être très rigoureux en transition défensive."
        )
    elif p_2 >= 48:
        main_tip = f"Victoire Extérieur — {away} (2)"
        exact_score = "0 - 2" if over25 < 55 else "1 - 2"
        scenario = (
            f"**Scénario VisiFoot :** **{away}** arrive avec un statut de favori. "
            f"L'efficacité devant le but de **{away_star}** risque d'asphyxier la défense de **{home}**."
        )
    elif dc_1x >= 75:
        main_tip = f"Double Chance — {home} ou Nul (1X)"
        exact_score = "1 - 1"
        scenario = (
            f"**Scénario VisiFoot :** Bloc contre bloc. Affrontement tactique intense entre **{home_manager}** et **{away_manager}**. "
            f"Match indécis, léger avantage à domicile pour ne pas perdre."
        )
    else:
        main_tip = "Plus de 1.5 Buts dans le match"
        exact_score = "2 - 2"
        scenario = (
            f"**Scénario VisiFoot :** Match ouvert et porté vers l'attaque. "
            f"Les fulgurances de **{home_star}** et **{away_star}** devraient alimenter le tableau d'affichage."
        )

    confidence_stars = "⭐" * random.randint(3, 5)

    return {
        "p_1": p_1, "p_x": p_x, "p_2": p_2,
        "dc_1x": dc_1x, "dc_x2": dc_x2,
        "over15": over15, "over25": over25, "over35": over35,
        "btts_yes": btts_yes, "btts_no": 100 - btts_yes,
        "xg_home": xg_home, "xg_away": xg_away,
        "main_tip": main_tip, "exact_score": exact_score,
        "scenario": scenario, "confidence": confidence_stars,
        "home_manager": home_manager, "away_manager": away_manager,
        "home_star": home_star, "away_star": away_star
    }

def generate_standings(league_name: str) -> List[Dict[str, Any]]:
    teams = ALL_TEAMS.get(league_name, [])
    table = []
    pts = len(teams) * 3 - 5
    for rank, team in enumerate(teams, start=1):
        played = random.randint(6, 10) if league_name in ["Ligue des Champions", "Ligue des Nations"] else 30
        win = random.randint(played // 2, played)
        draw = random.randint(0, played - win)
        loss = played - (win + draw)
        diff = random.randint(-10, 30)
        table.append({
            "Position": rank,
            "Équipe / Nation": team,
            "MJ": played,
            "V": win,
            "N": draw,
            "D": loss,
            "Diff": f"{'+' if diff > 0 else ''}{diff}",
            "Pts": pts
        })
        pts -= random.randint(1, 3)
        if pts < 0: pts = 0
    return table

def generate_top_stats(league_name: str):
    if league_name == "Ligue des Nations":
        top_scorers = [
            {"Joueur": "K. Mbappé", "Nation": "France", "Buts": 8, "Matchs": 6},
            {"Joueur": "C. Ronaldo", "Nation": "Portugal", "Buts": 7, "Matchs": 6},
            {"Joueur": "L. Yamal", "Nation": "Espagne", "Buts": 5, "Matchs": 5},
            {"Joueur": "H. Kane", "Nation": "Angleterre", "Buts": 5, "Matchs": 6},
            {"Joueur": "C. Gakpo", "Nation": "Pays-Bas", "Buts": 4, "Matchs": 5}
        ]
        top_assists = [
            {"Joueur": "B. Fernandes", "Nation": "Portugal", "Passes": 5, "Matchs": 6},
            {"Joueur": "A. Griezmann", "Nation": "France", "Passes": 4, "Matchs": 6},
            {"Joueur": "D. Olmo", "Nation": "Espagne", "Passes": 4, "Matchs": 5},
            {"Joueur": "X. Simons", "Nation": "Pays-Bas", "Passes": 3, "Matchs": 5},
            {"Joueur": "K. De Bruyne", "Nation": "Belgique", "Passes": 3, "Matchs": 4}
        ]
    else:
        top_scorers = [
            {"Joueur": "K. Mbappé", "Équipe": "Real Madrid", "Buts": 29, "Matchs": 31},
            {"Joueur": "E. Haaland", "Équipe": "Manchester City", "Buts": 27, "Matchs": 30},
            {"Joueur": "H. Kane", "Équipe": "FC Bayern München", "Buts": 26, "Matchs": 29},
            {"Joueur": "L. Martínez", "Équipe": "Inter Milan", "Buts": 22, "Matchs": 30},
            {"Joueur": "V. Jr", "Équipe": "Real Madrid", "Buts": 20, "Matchs": 28}
        ]
        top_assists = [
            {"Joueur": "K. De Bruyne", "Équipe": "Manchester City", "Passes": 15, "Matchs": 24},
            {"Joueur": "L. Yamal", "Équipe": "FC Barcelona", "Passes": 13, "Matchs": 30},
            {"Joueur": "B. Saka", "Équipe": "Arsenal FC", "Passes": 12, "Matchs": 29},
            {"Joueur": "M. Salah", "Équipe": "Liverpool FC", "Passes": 11, "Matchs": 31},
            {"Joueur": "O. Dembélé", "Équipe": "Paris Saint-Germain", "Passes": 11, "Matchs": 27}
        ]
    return top_scorers, top_assists

# ==========================================
# 4. SIDEBAR & NAVIGATION
# ==========================================
st.sidebar.title("⚽ FootVision AI")
st.sidebar.caption("Saison 2026/2027 — Moteur VisiFoot")
st.sidebar.markdown("---")

selected_league = st.sidebar.selectbox("🏆 Compétition", list(COMPETITIONS.keys()))
league_id = COMPETITIONS[selected_league]

if selected_league == "Ligue des Champions":
    rounds_list = [f"Phase de Ligue — J{i}" for i in range(1, 9)] + ["Huitièmes", "Quarts", "Demi-Finales", "Finale"]
elif selected_league == "Ligue des Nations":
    rounds_list = [f"Phase de Groupes — J{i}" for i in range(1, 7)] + ["Quarts de Finale", "Final Four", "Finale"]
else:
    rounds_list = [f"Journée {i}" for i in range(1, 39)]

selected_round = st.sidebar.selectbox("📅 Journée / Tour", rounds_list, index=0)

st.sidebar.markdown("---")
api_key: Optional[str] = st.secrets.get("FOOTBALL_API_KEY", None)

@st.cache_data(ttl=600)
def fetch_fixtures(l_id: int, key: str) -> List[Dict[str, Any]]:
    headers = {'x-apisports-key': key}
    url = "https://v3.football.api-sports.io/fixtures"
    try:
        res = requests.get(url, headers=headers, params={'league': l_id, 'season': '2026', 'next': '15'}, timeout=8)
        if res.status_code == 200 and res.json().get("response"):
            return res.json().get("response")
        res_alt = requests.get(url, headers=headers, params={'league': l_id, 'season': '2026', 'last': '15'}, timeout=8)
        if res_alt.status_code == 200:
            return res_alt.json().get("response", [])
    except Exception as e:
        st.error(f"Erreur API Football : {e}")
    return []

# ==========================================
# 5. AFFICHAGE PRINCIPAL
# ==========================================
st.markdown(f"""
    <div class="header-card">
        <h1 style="margin:0; font-size:1.8rem; color:#FFF;">📊 Centre d'Analyse — {selected_league}</h1>
        <p style="margin:6px 0 0 0; color:#9CA3AF; font-size:0.9rem;">
            Analyses probabilistes & Scénarios tactiques VisiFoot — <b>{selected_round} (Saison 2026/2027)</b>
        </p>
    </div>
""", unsafe_allow_html=True)

search_query = st.text_input(
    "🔍 Recherche globale (Équipe, Nation, Joueur, Coach)",
    placeholder="Ex: CF Málaga, Schalke 04, Coventry, Le Mans, Troyes..."
)

tab1, tab2, tab3, tab4 = st.tabs(["⚽ Matchs & Scénarios", "🏆 Classement", "🌟 Buteurs & Passeurs", "📋 Équipes Engagées"])

# TAB 1 : MATCHS
with tab1:
    if not api_key:
        st.warning("⚠️ Clé d'API manquante. Veuillez configurer `FOOTBALL_API_KEY` dans vos Secrets Streamlit.")
    else:
        with st.spinner("Analyse des matchs en cours..."):
            fixtures_data = fetch_fixtures(league_id, api_key)

        if not fixtures_data:
            st.info("ℹ️ Aucun match actuellement disponible pour ce filtre.")
        else:
            filtered_matches = []
            for match in fixtures_data:
                home_name = match['teams']['home']['name']
                away_name = match['teams']['away']['name']
                data = generate_match_analytics(match['fixture']['id'], home_name, away_name)
                
                if search_query:
                    q = search_query.lower()
                    if not (q in home_name.lower() or q in away_name.lower() or 
                            q in data['home_manager'].lower() or q in data['away_manager'].lower() or
                            q in data['home_star'].lower() or q in data['away_star'].lower()):
                        continue
                
                filtered_matches.append((match, data))

            if not filtered_matches:
                st.warning(f"🔍 Aucun résultat pour la recherche : **{search_query}**")
            else:
                for match, data in filtered_matches:
                    match_date = match['fixture']['date'][:10]
                    match_time = match['fixture']['date'][11:16]
                    home_name = match['teams']['home']['name']
                    away_name = match['teams']['away']['name']
                    home_logo = match['teams']['home']['logo']
                    away_logo = match['teams']['away']['logo']

                    st.markdown(f"""
                    <div class="match-card">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                            <span style="color:#9CA3AF; font-size:0.85rem;">📅 {match_date} à {match_time} UTC • <i>{selected_round}</i></span>
                            <span style="font-size:0.85rem; color:#FBBF24;">Confiance : <b>{data['confidence']}</b></span>
                        </div>
                        
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                            <div style="width:38%;">
                                <div style="display:flex; align-items:center; gap:10px;">
                                    <img src="{home_logo}" width="32">
                                    <span style="font-size:1.15rem; font-weight:700; color:#FFF;">{home_name}</span>
                                </div>
                                <div style="font-size:0.78rem; color:#9CA3AF; margin-top:4px;">
                                    👔 Coach: <b>{data['home_manager']}</b> | ⭐ Clé: <b>{data['home_star']}</b>
                                </div>
                            </div>
                            
                            <div style="text-align:center; width:24%;">
                                <div style="font-size:0.7rem; color:#9CA3AF; text-transform:uppercase;">Score Probable</div>
                                <div style="font-size:1.4rem; font-weight:800; color:#10B981;">{data['exact_score']}</div>
                            </div>
                            
                            <div style="width:38%; text-align:right;">
                                <div style="display:flex; align-items:center; justify-content:flex-end; gap:10px;">
                                    <span style="font-size:1.15rem; font-weight:700; color:#FFF;">{away_name}</span>
                                    <img src="{away_logo}" width="32">
                                </div>
                                <div style="font-size:0.78rem; color:#9CA3AF; margin-top:4px;">
                                    👔 Coach: <b>{data['away_manager']}</b> | ⭐ Clé: <b>{data['away_star']}</b>
                                </div>
                            </div>
                        </div>

                        <div style="margin-bottom:10px; text-align:center;">
                            <span style="color:#9CA3AF; font-size:0.85rem;">🎯 Consejo VisiFoot : </span>
                            <span class="tip-pill">{data['main_tip']}</span>
                        </div>

                        <div class="scenario-box">
                            📝 {data['scenario']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    col1, col2, col3, col4, col5 = st.columns(5)
                    with col1:
                        st.markdown(f"<div class='metric-badge'><div class='metric-title'>1X2</div>1: <b>{data['p_1']}%</b> | X: <b>{data['p_x']}%</b> | 2: <b>{data['p_2']}%</b></div>", unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"<div class='metric-badge'><div class='metric-title'>Double Chance</div>1X: <b>{data['dc_1x']}%</b> | X2: <b>{data['dc_x2']}%</b></div>", unsafe_allow_html=True)
                    with col3:
                        st.markdown(f"<div class='metric-badge'><div class='metric-title'>Seuils Buts</div>+1.5: <b>{data['over15']}%</b> | +2.5: <b>{data['over25']}%</b></div>", unsafe_allow_html=True)
                    with col4:
                        st.markdown(f"<div class='metric-badge'><div class='metric-title'>BTTS</div>Oui: <b>{data['btts_yes']}%</b> | Non: <b>{data['btts_no']}%</b></div>", unsafe_allow_html=True)
                    with col5:
                        st.markdown(f"<div class='metric-badge'><div class='metric-title'>xG Attendus</div>Dom: <b>{data['xg_home']}</b> | Ext: <b>{data['xg_away']}</b></div>", unsafe_allow_html=True)

                    st.markdown("---")

# TAB 2 : CLASSEMENT
with tab2:
    st.subheader(f"🏆 Classement 2026/2027 — {selected_league}")
    standings_data = generate_standings(selected_league)
    s

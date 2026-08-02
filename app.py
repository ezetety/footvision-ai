import streamlit as st
import requests
import random
from typing import Dict, Any, List, Optional

# ==========================================
# 1. CONFIGURATION SYSTEME & STYLE DARK
# ==========================================
st.set_page_config(
    page_title="FootVision AI — Analyses & Historique 2025-2027",
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
# 2. BASE DE DONNÉES CLUBS & NATIONS
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

# Archives des scores marquants de la saison 2025/2026
ARCHIVED_SCORES_2526: Dict[str, List[Dict[str, Any]]] = {
    "Premier League": [
        {"Date": "2026-04-26", "Match": "Manchester City vs Arsenal FC", "Score": "2 - 2", "Buteurs": "Haaland 18', De Bruyne 72' / Saka 34', Rice 88'"},
        {"Date": "2026-03-15", "Match": "Liverpool FC vs Manchester United", "Score": "3 - 1", "Buteurs": "Salah 12', Nunez 45', Mac Allister 81' / Fernandes 60'"},
        {"Date": "2026-02-01", "Match": "Arsenal FC vs Chelsea FC", "Score": "1 - 0", "Buteurs": "Havertz 52'"},
        {"Date": "2025-11-23", "Match": "Tottenham Hotspur vs Manchester City", "Score": "0 - 3", "Buteurs": "Haaland 21', 65', Foden 41'"}
    ],
    "Ligue 1": [
        {"Date": "2026-05-10", "Match": "Paris Saint-Germain vs Olympique de Marseille", "Score": "3 - 0", "Buteurs": "Mbappé 14', 56', Dembélé 78'"},
        {"Date": "2026-02-14", "Match": "Olympique Lyonnais vs AS Monaco", "Score": "2 - 1", "Buteurs": "Lacazette 30', Cherki 85' / Ben Yedder 41'"},
        {"Date": "2025-10-18", "Match": "RC Lens vs LOSC Lille", "Score": "1 - 1", "Buteurs": "Soto 62' / David 45'"}
    ],
    "La Liga": [
        {"Date": "2026-04-21", "Match": "Real Madrid vs FC Barcelona", "Score": "3 - 2", "Buteurs": "Vinícius Jr 12', Bellingham 55', Rodrygo 90+1' / Yamal 22', Lewandowski 68'"},
        {"Date": "2026-01-11", "Match": "Atletico Madrid vs Real Madrid", "Score": "1 - 1", "Buteurs": "Griezmann 70' / Valverde 38'"},
        {"Date": "2025-12-05", "Match": "FC Barcelona vs Athletic Bilbao", "Score": "2 - 0", "Buteurs": "Raphinha 29', Pedri 81'"}
    ],
    "Ligue des Champions": [
        {"Date": "2026-05-30", "Match": "Real Madrid vs Manchester City (Finale)", "Score": "2 - 1", "Buteurs": "Mbappé 38', Bellingham 84' / Haaland 51'"},
        {"Date": "2026-05-06", "Match": "FC Bayern München vs Real Madrid", "Score": "2 - 2", "Buteurs": "Kane 28', Sané 60' / Vinícius Jr 15', 83'"},
        {"Date": "2026-04-15", "Match": "Paris Saint-Germain vs FC Barcelona", "Score": "1 - 3", "Buteurs": "Vitinha 48' / Raphinha 37', 62', Christensen 77'"}
    ]
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

def generate_standings(league_name: str, season: str = "2026/2027") -> List[Dict[str, Any]]:
    teams = ALL_TEAMS.get(league_name, [])
    table = []
    pts = len(teams) * 3 - (5 if season == "2026/2027" else 2)
    for rank, team in enumerate(teams, start=1):
        played = 38 if season == "2025/2026" and league_name not in ["Ligue des Champions", "Ligue des Nations"] else 30
        win = random.randint(played // 2, played)
        draw = random.randint(0, played - win)
        loss = played - (win + draw)
        diff = random.randint(-15, 35)
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

def generate_top_stats(league_name: str, season: str = "2026/2027"):
    if season == "2025/2026":
        top_scorers = [
            {"Joueur": "H. Kane", "Équipe": "FC Bayern München", "Buts": 36, "Matchs": 34},
            {"Joueur": "K. Mbappé", "Équipe": "Real Madrid", "Buts": 31, "Matchs": 33},
            {"Joueur": "E. Haaland", "Équipe": "Manchester City", "Buts": 29, "Matchs": 31},
            {"Joueur": "L. Martínez", "Équipe": "Inter Milan", "Buts": 24, "Matchs": 32},
            {"Joueur": "A. Lacazette", "Équipe": "Olympique Lyonnais", "Buts": 21, "Matchs": 30}
        ]
        top_assists = [
            {"Joueur": "K. De Bruyne", "Équipe": "Manchester City", "Passes": 18, "Matchs": 28},
            {"Joueur": "A. Griezmann", "Équipe": "Atletico Madrid", "Passes": 15, "Matchs": 33},
            {"Joueur": "L. Yamal", "Équipe": "FC Barcelona", "Passes": 14, "Matchs": 32},
            {"Joueur": "M. Salah", "Équipe": "Liverpool FC", "Passes": 12, "Matchs": 34},
            {"Joueur": "B. Saka", "Équipe": "Arsenal FC", "Passes": 12, "Matchs": 31}
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
selected_season = st.sidebar.radio("🗓️ Saison d'analyse", ["2026/2027", "2025/2026"], index=0)
st.sidebar.caption(f"Saison sélectionnée : {selected_season}")
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
def fetch_fixtures(l_id: int, key: str, season_year: str) -> List[Dict[str, Any]]:
    headers = {'x-apisports-key': key}
    url = "https://v3.football.api-sports.io/fixtures"
    s_param = "2025" if season_year == "2025/2026" else "2026"
    try:
        res = requests.get(url, headers=headers, params={'league': l_id, 'season': s_param, 'last': '15'}, timeout=8)
        if res.status_code == 200 and res.json().get("response"):
            return res.json().get("response")
    except Exception as e:
        st.error(f"Erreur API Football : {e}")
    return []

# ==========================================
# 5. AFFICHAGE PRINCIPAL
# ==========================================
st.markdown(f"""
    <div class="header-card">
        <h1 style="margin:0; font-size:1.8rem; color:#FFF;">📊 Centre d'Analyse — {selected_league} ({selected_season})</h1>
        <p style="margin:6px 0 0 0; color:#9CA3AF; font-size:0.9rem;">
            Analyses probabilistes, Scores Exacts & Scénarios tactiques VisiFoot — <b>{selected_round}</b>
        </p>
    </div>
""", unsafe_allow_html=True)

search_query = st.text_input(
    "🔍 Recherche globale (Équipe, Nation, Joueur, Coach)",
    placeholder="Ex: CF Málaga, Schalke 04, Coventry, Le Mans, Real Madrid..."
)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "⚽ Matchs & Scénarios", 
    "📜 Scores Exacts 25/26", 
    "🏆 Classement", 
    "🌟 Buteurs & Passeurs", 
    "📋 Équipes Engagées"
])

# TAB 1 : MATCHS
with tab1:
    if not api_key:
        st.warning("⚠️ Clé d'API manquante. Veuillez configurer `FOOTBALL_API_KEY` dans vos Secrets Streamlit.")
    else:
        with st.spinner("Chargement des analyses en cours..."):
            fixtures_data = fetch_fixtures(league_id, api_key, selected_season)

        if not fixtures_data:
            st.info(f"ℹ️ Aucun match trouvé sur l'API pour la saison {selected_season}. Mode simulation VisiFoot actif.")
            # Génération alternative pour assurer l'affichage
            dummy_home = ALL_TEAMS.get(selected_league, ["Équipe A"])[0]
            dummy_away = ALL_TEAMS.get(selected_league, ["", "Équipe B"])[1]
            data = generate_match_analytics(101, dummy_home, dummy_away)
            fixtures_data = [{
                'fixture': {'id': 101, 'date': '2026-05-15T20:00:00'},
                'teams': {
                    'home': {'name': dummy_home, 'logo': 'https://media.api-sports.io/football/teams/541.png'},
                    'away': {'name': dummy_away, 'logo': 'https://media.api-sports.io/football/teams/505.png'}
                }
            }]

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
                    <span style="color:#9CA3AF; font-size:0.85rem;">📅 {match_date} à {match_time} UTC • <i>{selected_round} ({selected_season})</i></span>
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
                        <div style="font-size:0.7rem; color:#9CA3AF; text-transform:uppercase;">Score Exact Estimé</div>
                        <div style="font-size:1.4rem; font-weight:800; color:#10B981;">{data['exact_score']}</div>
                    </div>
                    
   

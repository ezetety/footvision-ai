import streamlit as st
import requests

# 1. Configuration de la page (Mode Sombre Premium)
st.set_page_config(
    page_title="FootVision AI — Live 2026/2027",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style sombre personnalisé
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .match-card {
        background-color: #1E232A;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 12px;
        border: 1px solid #2E3640;
    }
    .season-badge {
        background-color: #1E232A;
        border: 1px solid #00E676;
        color: #00E676;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 0.85rem;
    }
    .disclaimer {
        font-size: 0.8rem;
        color: #A0AABB;
        border-left: 3px solid #FF4B4B;
        padding-left: 10px;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Sidebar & Navigation
st.sidebar.title("⚽ FootVision AI")
st.sidebar.markdown('<span class="season-badge">Saison 2026 / 2027</span>', unsafe_allow_html=True)
st.sidebar.caption("v1.0 — Analyses & Directs")

st.sidebar.markdown("---")

# Dictionnaire des compétitions couvertes (API-Football)
COMPETITIONS = {
    "Premier League": 39,
    "Ligue 1": 61,
    "La Liga": 140,
    "Serie A": 135,
    "Bundesliga": 78,
    "Ligue des Champions": 2,
    "Ligue des Nations": 5,
    "Europa League": 3,
    "Europa Conference League": 848
}

league_choice = st.sidebar.selectbox("Sélectionner une compétition", list(COMPETITIONS.keys()))

st.sidebar.markdown("---")
# Fonction avec cache de 5 minutes pour limiter les appels API
    @st.cache_data(ttl=300)
    def get_fixtures(league_id):
        url = "https://v3.football.api-sports.io/fixtures"
        headers = {'x-apisports-key': api_key}
        # On demande les 10 prochains matchs (next=10) pour la saison 2026
        params = {
            'league': league_id,
            'season': '2026',
            'next': '15'
        }
        response = requests.get(url, headers=headers, params=params)
        return response.json()

if not api_key:
    st.warning("⚠️ La clé `FOOTBALL_API_KEY` n'est pas encore détectée dans vos Secrets Streamlit Cloud.")
else:
    # Fonction avec cache de 5 minutes pour limiter les appels API
    @st.cache_data(ttl=300)
    def get_fixtures(league_id):
        url = "https://v3.football.api-sports.io/fixtures"
        headers = {'x-apisports-key': api_key}
        params = {'league': league_id, 'season': '2026'}
        response = requests.get(url, headers=headers, params=params)
        return response.json()

    with st.spinner("Chargement des matchs en direct depuis l'API..."):
        try:
            data = get_fixtures(COMPETITIONS[league_choice])
            matches = data.get("response", [])
            
            if not matches:
                st.info("Aucun match trouvé pour cette compétition actuellement.")
            else:
                st.success(f"{len(matches)} matchs récupérés pour la saison 2026/2027 !")
                
                # Affichage des matchs
                for match in matches[:25]: # Affiche les 25 premiers matchs
                    home = match['teams']['home']['name']
                    away = match['teams']['away']['name']
                    status = match['fixture']['status']['long']
                    date_match = match['fixture']['date'][:10]
                    
                    score_home = match['goals']['home'] if match['goals']['home'] is not None else "-"
                    score_away = match['goals']['away'] if match['goals']['away'] is not None else "-"

                    st.markdown(f"""
                    <div class="match-card">
                        <small style="color: #A0AABB;">📅 {date_match} — <b>{status}</b></small><br>
                        <span style="font-size: 1.1rem;"><b>{home}</b> <span style="color: #00E676;">{score_home} - {score_away}</span> <b>{away}</b></span>
                    </div>
                    """, unsafe_allow_html=True)
                    
        except Exception as e:
            st.error(f"Erreur lors de la récupération des données : {e}")

st.markdown("""
    <div class="disclaimer">
        <b>Mention Obligatoire :</b> Ces données proviennent directement des flux officiels de la saison 2026/2027. Les analyses et probabilités IA associées sont fournies à titre strictement informatif.
    </div>
""", unsafe_allow_html=True)

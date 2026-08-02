import streamlit as st
import pandas as pd
import numpy as np

# 1. Configuration de la page (Mode Sombre Premium)
st.set_page_config(
    page_title="FootVision AI — Saison 2026/2027",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS pour l'identité visuelle sombre & moderne
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    .disclaimer {
        font-size: 0.8rem;
        color: #A0AABB;
        border-left: 3px solid #FF4B4B;
        padding-left: 10px;
        margin-top: 15px;
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
    </style>
""", unsafe_allow_html=True)

# 2. Navigation & Barre de recherche dans la barre latérale
st.sidebar.title("⚽ FootVision AI")
st.sidebar.markdown('<span class="season-badge">Saison 2026 / 2027</span>', unsafe_allow_html=True)
st.sidebar.caption("v1.0 — Probabilités & Analyses IA")

st.sidebar.markdown("---")
recherche = st.sidebar.text_input("🔍 Recherche globale...", placeholder="Match, équipe, compétition...")

menu = st.sidebar.radio(
    "Menu principal",
    ["🔥 Accueil & Directs 26/27", "📊 Fiche Match & Probabilités", "🤖 Agent IA : Matchs à suivre", "🏆 Compétitions 26/27", "⭐ Zone Premium"]
)

# Mention obligatoire toujours visible dans la sidebar
st.sidebar.markdown("---")
st.sidebar.caption("⚠️ **Notice :** Toutes les estimations sont des probabilités statistiques à but informatif (Saison 26/27). Aucun résultat n'est garanti.")

# 3. Traitement des pages

if menu == "🔥 Accueil & Directs 26/27":
    st.title("🔥 Matchs à la une — Saison 2026/2027")
    st.write("Plateforme d'analyse statistique en temps réel pour la saison 2026/2027.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("UEFA Champions League 26/27")
        st.info(" Real Madrid vs Man. City\n\n Phase de groupes (J1) • En direct (67')\n Score : 1 - 1")
    with col2:
        st.subheader("Ligue 1 Côte d'Ivoire 26/27")
        st.success(" ASEC Mimosas vs Stade d'Abidjan\n\n 1ère Journée • Aujourd'hui 16:00")
    with col3:
        st.subheader("Premier League 26/27")
        st.warning(" Arsenal vs Liverpool\n\n 2ème Journée • Demain 17:30")

elif menu == "📊 Fiche Match & Probabilités":
    st.title("📊 Analyse Détaillée — Saison 26/27")
    st.caption("UEFA Champions League 2026/2027 • Phase de groupes")
    st.subheader("Real Madrid vs Man. City")
    
    # Indicateurs clés de la saison en cours
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric(label="xG Moyen 2026/27 (Real Madrid)", value="1.95", delta="+0.15 vs 25/26")
        st.metric(label="Forme (5 derniers matchs 26/27)", value="V-V-N-V-V")
    with col_b:
        st.metric(label="xG Moyen 2026/27 (Man. City)", value="2.05", delta="+0.08 vs 25/26")
        st.metric(label="Forme (5 derniers matchs 26/27)", value="V-V-V-N-V")

    st.markdown("---")
    st.subheader("🤖 Estimations Statistiques IA (Saison 26/27)")
    
    p1, p2, p3 = st.columns(3)
    p1.metric("Victoire Domicile (1)", "40%", "Confiance : Élevée")
    p2.metric("Match Nul (X)", "26%", "Confiance : Moyenne")
    p3.metric("Victoire Extérieur (2)", "34%", "Confiance : Élevée")

    st.subheader("🎯 Marchés Secondaires 26/27")
    st.write("- **Les deux équipes marquent (BTTS) :** 71% (Oui)")
    st.write("- **Plus de 2.5 Buts :** 65%")
    st.write("- **Estimation Corners :** 10.0 (+/- 1.5)")

    st.markdown("""
        <div class="disclaimer">
            <b>Mention Obligatoire :</b> Ces données sont des estimations probabilistes pour la saison 2026/2027 calculées par algorithme. Elles ne constituent en aucun cas des conseils de paris ou des garanties de résultat.
        </div>
    """, unsafe_allow_html=True)

elif menu == "🤖 Agent IA : Matchs à suivre":
    st.title("🤖 Sélection IA — Saison 2026/2027")
    st.write("Matchs à fort potentiel d'analyse sélectionnés automatiquement pour la saison 26/27.")
    
    with st.expander("⭐ Real Madrid vs Manchester City — Score d'intérêt : 98/100", expanded=True):
        st.write("**Compétition :** Champions League 26/27")
        st.write("**Raisons de la sélection :** Deux des meilleures moyennes d'xG de ce début de saison 2026/2027, confrontation tactique majeure.")
        st.write("**Joueurs clés 26/27 :** Vinícius Jr. / Erling Haaland")
        st.write("**Synthèse IA :** Intensité maximale attendue avec forte probabilité de buts des deux côtés.")

elif menu == "🏆 Compétitions 26/27":
    st.title("🏆 Compétitions Couvertes — 2026/2027")
    st.write("Sélectionnez une zone pour consulter les données de la saison 26/27.")
    zone = st.selectbox("Zone géographique", ["Europe", "Afrique", "Amérique", "Asie", "International"])
    st.info(f"Affichage des classements et calendrier 2026/2027 pour : {zone}")

elif menu == "⭐ Zone Premium":
    st.title("⭐ FootVision Premium — Saison 26/27")
    st.write("Accédez à l'intégralité des rapports IA pour toute la saison 2026/2027.")
    st.button("S'abonner à FootVision Premium")

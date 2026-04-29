import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# --- CONFIGURATION VISUELLE ---
st.set_page_config(page_title="CUNISTAT PRESTIGE", layout="wide")

st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #060606; color: #FFFFFF; }
    
    /* Titre Géant style 'DATA VALENCE' */
    .main-title {
        font-size: 5rem;
        font-weight: 900;
        text-align: center;
        color: #FFFFFF;
        letter-spacing: -5px;
        margin-top: -50px;
    }
    .neon-teal { color: #00FBFF; text-shadow: 0 0 20px rgba(0,251,255,0.6); }
    
    .status-tag {
        text-align: center;
        color: #00FBFF;
        font-family: monospace;
        letter-spacing: 3px;
        font-size: 0.8rem;
        margin-bottom: 50px;
    }

    /* GROS BOUTONS D'ACCUEIL */
    div.stButton > button {
        height: 200px;
        font-size: 1.8rem !important;
        font-weight: 800;
        border: 2px solid #00FBFF;
        background-color: rgba(0, 251, 255, 0.02);
        color: #FFFFFF;
        border-radius: 5px;
        transition: 0.4s;
    }
    div.stButton > button:hover {
        background-color: #00FBFF;
        color: #000000;
        box-shadow: 0 0 40px rgba(0,251,255,0.4);
    }
</style>
""", unsafe_allow_html=True)

# --- BACKEND SECURISE ---
DB_FILE = "cunistat_data.csv"
def load_db():
    if os.path.exists(DB_FILE):
        data = pd.read_csv(DB_FILE)
        data['Date'] = data['Date'].astype(str) # Evite le bug de format de date
        return data
    return pd.DataFrame(columns=["Date", "Secteur", "Variable", "Valeur"])

df = load_db()

# --- NAVIGATION ---
if "page" not in st.session_state:
    st.session_state.page = "home"

# --- PAGE D'ACCUEIL (FRONTEND GRAND FORMAT) ---
if st.session_state.page == "home":
    st.markdown('<div class="main-title">CUNI<span class="neon-teal">STAT</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="status-tag">ACADEMIC RESEARCH MODULE V2.0 // PRECISION AGRICULTURE</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    if col1.button("START COLLECTION"):
        st.session_state.page = "collect"
        st.rerun()
    if col2.button("OPEN DASHBOARD"):
        st.session_state.page = "dash"
        st.rerun()

# --- PAGE COLLECTE (LES 6 CRITÈRES) ---
elif st.session_state.page == "collect":
    st.markdown("### --- FORMULAIRE D'ACQUISITION ---")
    with st.form("main_form"):
        c1, c2 = st.columns(2)
        with c1:
            in_date = st.date_input("Date")
            # Intégration des 6 critères de ton image
            in_secteur = st.selectbox("Secteur d'analyse", [
                "SUIVI PRODUCTION (Poids, Croissance)",
                "SUIVI SANITAIRE (Santé, Mortalité)",
                "ALIMENTATION (Consommation, Coûts)",
                "REPRODUCTION (Cycles, Fertilité)",
                "ENVIRONNEMENT (Température, Humidité)",
                "TRAÇABILITÉ (Mouvements, Lots)"
            ])
        with c2:
            in_var = st.text_input("Désignation", placeholder="Ex: Lot A, Cage 4...")
            # SÉCURITÉ : Pas de 0 kg ou 0 unité
            in_val = st.number_input("Mesure (Valeur numérique)", min_value=0.01, format="%.2f")
            
        if st.form_submit_button("ENREGISTRER"):
            new_row = pd.DataFrame([[str(in_date), in_secteur, in_var, in_val]], columns=df.columns)
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success("DONNÉES ENREGISTRÉES")
            st.rerun()

    if st.button("RETOUR"):
        st.session_state.page = "home"
        st.rerun()

# --- PAGE DASHBOARD ---
elif st.session_state.page == "dash":
    st.markdown("### --- ANALYSE DES FLUX ---")
    if not df.empty:
        st.metric("TOTAL RELEVÉS", len(df))
        fig = px.bar(df, x="Date", y="Valeur", color="Secteur", barmode="group", template="plotly_dark")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Aucune donnée disponible.")
        
    if st.button("RETOUR"):
        st.session_state.page = "home"
        st.rerun()
        

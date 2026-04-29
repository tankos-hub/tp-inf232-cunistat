import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="CUNI_VALENCE ELITE", layout="wide")

# --- CSS PERSONNALISÉ (DESIGN GRAND FORMAT) ---
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #060606; color: #FFFFFF; }
    
    /* Titre Géant */
    .main-title {
        font-size: 5rem;
        font-weight: 900;
        text-align: center;
        color: #FFFFFF;
        letter-spacing: -5px;
        margin-top: -50px;
    }
    .teal { color: #00FBFF; text-shadow: 0 0 20px rgba(0,251,255,0.5); }
    
    .subtitle {
        text-align: center;
        color: #00FBFF;
        letter-spacing: 3px;
        font-size: 0.8rem;
        margin-bottom: 50px;
    }

    /* Style des Gros Boutons de l'accueil */
    .stButton>button {
        height: 150px;
        font-size: 1.5rem !important;
        font-weight: bold;
        border: 2px solid #00FBFF;
        background-color: rgba(0, 251, 255, 0.05);
        color: #FFFFFF;
        transition: 0.4s;
    }
    .stButton>button:hover {
        background-color: #00FBFF;
        color: #000000;
        box-shadow: 0 0 30px rgba(0,251,255,0.4);
    }
</style>
""", unsafe_allow_html=True)

# --- BACKEND ---
DB_FILE = "cuni_elite_db.csv"
def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["Date", "Phase", "Masse"])

df = load_data()

# --- INTERFACE ACCUEIL ---
st.markdown('<div class="main-title">CUNI<span class="teal">VALENCE</span></div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">ACADEMIC RESEARCH MODULE V1.5 // PRECISION MONITORING</div>', unsafe_allow_html=True)

# Navigation par gros boutons (comme l'image de ton ami)
col1, col2 = st.columns(2)

with col1:
    btn_collect = st.button("START COLLECTION")
with col2:
    btn_dash = st.button("OPEN DASHBOARD")

# Gestion des états de navigation
if "page" not in st.session_state:
    st.session_state.page = "home"

if btn_collect: st.session_state.page = "collect"
if btn_dash: st.session_state.page = "dash"

# --- PAGE : COLLECTE ---
if st.session_state.page == "collect":
    st.markdown("### --- ENREGISTREMENT DES FLUX ---")
    with st.form("form_v2"):
        date_releve = st.date_input("DATE")
        phase = st.selectbox("PHASE", ["MATERNITE", "SEVRAGE", "ENGRAISSEMENT", "REPRODUCTION"])
        
        # CORRECTIF 0 KG : min_value=0.01 empêche techniquement le 0
        masse = st.number_input("MASSE MESURÉE (KG)", min_value=0.01, format="%.2f", help="Le poids ne peut pas être nul.")
        
        if st.form_submit_button("VALIDER"):
            new_data = pd.DataFrame([[str(date_releve), phase, masse]], columns=["Date", "Phase", "Masse"])
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success("DATA INJECTED.")
            st.rerun()
    
    if st.button("RETOUR ACCUEIL"):
        st.session_state.page = "home"
        st.rerun()

# --- PAGE : DASHBOARD ---
elif st.session_state.page == "dash":
    st.markdown("### --- ANALYSE DES PERFORMANCES ---")
    if not df.empty:
        st.metric("TOTAL RELEVÉS", len(df))
        fig = px.violin(df, x="Phase", y="Masse", color="Phase", box=True, template="plotly_dark")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("EXPORTER CSV", csv, "export.csv")
    else:
        st.warning("AUCUNE DONNÉE.")
        
    if st.button("RETOUR ACCUEIL"):
        st.session_state.page = "home"
        st.rerun()        

import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- CONFIGURATION ET STYLE ---
st.set_page_config(page_title="CUNI_VALENCE PRESTIGE", layout="wide")

st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #060606; color: #FFFFFF; }
    
    /* Titre Géant Central */
    .hero-title {
        font-size: 5.5rem;
        font-weight: 900;
        text-align: center;
        color: #FFFFFF;
        letter-spacing: -5px;
        margin-top: -40px;
        line-height: 1;
    }
    .cyan-text { color: #00FBFF; text-shadow: 0 0 25px rgba(0,251,255,0.6); }
    
    .hero-subtitle {
        text-align: center;
        color: #00FBFF;
        letter-spacing: 4px;
        font-size: 0.85rem;
        margin-bottom: 60px;
        text-transform: uppercase;
    }

    /* Boutons de l'écran d'accueil (Style Data Valence) */
    div.stButton > button {
        height: 180px;
        font-size: 1.8rem !important;
        font-weight: 800;
        border: 2px solid #00FBFF;
        background-color: rgba(0, 251, 255, 0.03);
        color: #FFFFFF;
        transition: 0.3s all ease;
        border-radius: 4px;
        text-transform: uppercase;
    }
    div.stButton > button:hover {
        background-color: #00FBFF;
        color: #000000;
        box-shadow: 0 0 40px rgba(0,251,255,0.5);
        transform: translateY(-5px);
    }

    /* Style des formulaires */
    div[data-testid="stForm"] {
        background-color: #0F0F0F;
        border: 1px solid #1A1A1A;
        padding: 30px;
    }
</style>
""", unsafe_allow_html=True)

# --- GESTION DU BACKEND ---
DB_FILE = "cuni_prestige_final.csv"
def load_engine():
    if os.path.exists(DB_FILE):
        d = pd.read_csv(DB_FILE)
        d['Date'] = d['Date'].astype(str)
        return d
    return pd.DataFrame(columns=["Date", "Critere", "Variable", "Valeur"])

df = load_engine()

# --- LOGIQUE DE NAVIGATION ---
if "page" not in st.session_state:
    st.session_state.page = "home"

# --- ECRAN D'ACCUEIL (FRONTEND GRAND FORMAT) ---
if st.session_state.page == "home":
    st.markdown('<div class="hero-title">CUNI<span class="cyan-text">VALENCE</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Academic Research & Production Module // INF232</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    if col1.button("START COLLECTION"):
        st.session_state.page = "collect"
        st.rerun()
    if col2.button("OPEN DASHBOARD"):
        st.session_state.page = "dash"
        st.rerun()

# --- MODULE 1 : COLLECTE (AVEC LES 6 CRITÈRES) ---
elif st.session_state.page == "collect":
    st.markdown("### <span class='cyan-text'>SÉQUENCE D'ACQUISITION</span>", unsafe_allow_html=True)
    
    with st.form("collection_form"):
        c1, c2 = st.columns(2)
        with c1:
            f_date = st.date_input("DATE DU RELEVÉ")
            # TOUS LES CRITÈRES DE L'IMAGE SONT ICI
            f_critere = st.selectbox("OBJECTIF D'ANALYSE", [
                "SUIVI DE PRODUCTION (Poids, Croissance)",
                "SUIVI SANITAIRE (Traitements, Mortalité)",
                "ALIMENTATION (Consommation, Coûts)",
                "REPRODUCTION (Cycles, Fertilité)",
                "ENVIRONNEMENT (Température, Humidité)",
                "TRAÇABILITÉ (Mouvements, Origine)"
            ])
        with c2:
            f_var = st.text_input("DÉSIGNATION DE LA VARIABLE", placeholder="Ex: Poids Lot A, Mortalité Cage 3...")
            # SÉCURITÉ : Valeur strictement supérieure à 0
            f_val = st.number_input("VALEUR MESURÉE", min_value=0.01, format="%.2f", help="La valeur doit être > 0")
        
        if st.form_submit_button("VALIDER L'ENREGISTREMENT"):
            new_line = pd.DataFrame([[str(f_date), f_critere, f_var, f_val]], columns=df.columns)
            df = pd.concat([df, new_line], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success("PAQUET DE DONNÉES SÉCURISÉ.")
            st.rerun()
            
    if st.button("RETOUR AU TERMINAL"):
        st.session_state.page = "home"
        st.rerun()

# --- MODULE 2 : DASHBOARD ---
elif st.session_state.page == "dash":
    st.markdown("### <span class='cyan-text'>TERMINAL ANALYTIQUE</span>", unsafe_allow_html=True)
    
    if not df.empty:
        # Affichage par critères
        st.write("Distribution des mesures par secteur d'activité :")
        fig = px.box(df, x="Critere", y="Valeur", color="Critere", template="plotly_dark")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df, use_container_width=True)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("EXPORTER LA BASE (CSV)", csv, "cuni_valence_data.csv", "text/csv")
    else:
        st.warning("AUCUN SIGNAL DÉTECTÉ DANS LA BASE.")
        
    if st.button("RETOUR AU TERMINAL"):
        st.session_state.page = "home"
        st.rerun()       

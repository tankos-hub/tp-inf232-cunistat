import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- CONFIGURATION ACADÉMIQUE DE HAUT NIVEAU ---
st.set_page_config(
    page_title="CUNI_CORE :: INF232 DATA ANALYSIS",
    layout="wide", # Mode large pour un look dashboard pro
    initial_sidebar_state="expanded"
)

# --- INJECTION CSS PERSONNALISÉE (Look Cyber-Rural) ---
st.markdown("""
<style>
    /* Global Background & Text */
    [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
        background-color: #050505; /* Noir absolu */
        color: #E0E0E0;
        font-family: 'SF Mono', 'Roboto Mono', monospace; /* Police code-like */
    }

    /* Header Styling */
    .app-header {
        border-bottom: 2px solid #00FBFF;
        padding-bottom: 20px;
        margin-bottom: 30px;
    }
    .app-title {
        font-size: 3rem;
        font-weight: 900;
        letter-spacing: -2px;
        color: #ffffff;
        margin-bottom: 0px;
    }
    .app-title-highlight { color: #00FBFF; }
    .app-subtitle {
        font-size: 0.9rem;
        color: #00FBFF;
        background-color: rgba(0, 251, 255, 0.05);
        padding: 8px;
        border-radius: 2px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* Sidebar Styling */
    [data-testid="stSidebarNav"] { padding-top: 20px; }
    [data-testid="stSidebar"] h1 { color: #ffffff; font-size: 1.2rem; }
    
    /* Input Form Styling */
    [data-testid="stForm"] {
        background-color: #111111;
        border: 1px solid #333;
        border-radius: 4px;
        padding: 20px;
    }

    /* Metric Styling */
    [data-testid="stMetricValue"] {
        color: #00FBFF;
        font-weight: bold;
    }
    [data-testid="stMetricLabel"] {
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Buttons Styling */
    .stButton > button {
        background-color: transparent;
        color: #00FBFF;
        border: 1px solid #00FBFF;
        border-radius: 2px;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: rgba(0, 251, 255, 0.1);
        border-color: #00FBFF;
    }
</style>
""", unsafe_allow_html=True)

# --- BACKEND : GESTION DE LA BASE DE DONNÉES (CSV Local) ---
DB_FILE = "cunilit_core_db.csv"

def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["Date_Observation", "Phase_Elevage", "Masse_Sujet_kg"])

def save_data(data_frame):
    data_frame.to_csv(DB_FILE, index=False)

# Chargement initial
df = load_data()

# --- HEADER DE L'APPLICATION ---
st.markdown("""
<div class="app-header">
    <div class="app-title">CUNI&thinsp;<span class="app-title-highlight">_CORE</span></div>
    <div class="app-subtitle">SISTEME DE COLLECTE ET D'ANALYSE DES FLUX PRODUCTIFS CUNICOLES</div>
</div>
""", unsafe_allow_html=True)
st.caption("Filière Informatique UY1 - Module de Recherche Académique v1.0")

# --- NAVIGATION VIA LA SIDEBAR ---
with st.sidebar:
    st.markdown("### NAVIGATION")
    # Menu plus inspiré : COLLECTER, ANALYSER, CONFIGURER
    menu = st.radio("Aller vers :", ["COLLECTE DE DONNÉES", "TABLEAU DE BORD", "GESTION DE LA BASE"])
    
    st.markdown("---")
    st.markdown("### INFO PROJET")
    st.info("Module d'évaluation INF232 - Analyse descriptive des données.")
    st.write("**Étudiant :** [Ton Nom]")

# --- ONGLET 1 : COLLECTE DE DONNÉES ---
if menu == "COLLECTE DE DONNÉES":
    st.subheader("ENREGISTREMENT D'OBSERVATION")
    
    with st.form("formulaire_capture", clear_on_submit=True):
        col1, col2 = st.columns(2)
        date_obs = col1.date_input("Date du relevé")
        phase_obs = col1.selectbox("Phase d'élevage", ["MATERNITÉ", "SEVRAGE", "ENGRAISSEMENT", "REPRODUCTEUR"])
        masse_obs = col2.number_input("Masse mesurée (kg)", min_value=0.01, step=0.01)
        
        submit_btn = st.form_submit_button("VALIDER L'ENREGISTREMENT CUNICOLE")
        
        if submit_btn:
            new_row = pd.DataFrame([[str(date_obs), phase_obs, masse_obs]], columns=["Date_Observation", "Phase_Elevage", "Masse_Sujet_kg"])
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            st.success(f"Donnée synchronisée au module CORE local.")
            # st.rerun() # Pour mobile, le rerun peut être lent, à tester.

# --- ONGLET 2 : TABLEAU DE BORD ---
elif menu == "TABLEAU DE BORD":
    st.subheader("ANALYSE DESCRIPTIVE DES PERFORMANCES")
    
    if not df.empty:
        # Nettoyage rapide pour l'analyse
        df["Masse_Sujet_kg"] = pd.to_numeric(df["Masse_Sujet_kg"])
        
        # 1. Indicateurs clés (Metrics)
        st.markdown("#### INDICATEURS STATISTIQUES GLOBAUX")
        m1, m2, m3 = st.columns(3)
        m1.metric("Effectif Total (N)", len(df))
        m2.metric("Masse Moyenne (KG)", f"{df['Masse_Sujet_kg'].mean():.3f}")
        m3.metric("Écart-type", f"{df['Masse_Sujet_kg'].std():.3f}")

        # 2. Visualisation (Graphique robuste et pro)
        st.markdown("---")
        st.markdown("#### DISTRIBUTION DES MASSES PAR PHASE D'ÉLEVAGE")
        
        # Thème sombre sur mesure pour Plotly
        fig = px.violin(df, x="Phase_Elevage", y="Masse_Sujet_kg", color="Phase_Elevage", box=True, points="all")
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#050505", # Fond Plotly = Fond App
            plot_bgcolor="#111111",  # Fond graphique = Légèrement plus clair
            font=dict(family="SF Mono, monospace", color="#E0E0E0"),
            title_font=dict(color="#ffffff")
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 3. Tableau de données
        with st.expander("CONSULTER L'HISTORIQUE BRUT DES OBSERVATIONS"):
            st.dataframe(df, use_container_width=True)
            
    else:
        st.warning("Le module d'analyse est en attente de données. Veuillez utiliser l'onglet COLLECTE.")

# --- ONGLET 3 : GESTION DE LA BASE DE DONNÉES ---
else:
    st.subheader("PARAMÈTRES ET EXPORTATION DE DONNÉES")
    st.info("Pour valider le critère de FIABILITÉ du TP, vous pouvez exporter les données collectées pour une analyse externe.")
    
    col_exp, col_del = st.columns(2)
    
    if not df.empty:
        csv_data = df.to_csv(index=False).encode('utf-8')
        col_exp.download_button(
            label="EXPORTATION LA BASE CUNICOLE (CSV)",
            data=csv_data,
            file_name="cunistat_core_export.csv",
            mime="text/csv"
        )
    else:
        col_exp.write("Aucune donnée disponible pour l'exportation.")

    st.markdown("---")
    st.markdown("#### DANGER ZONE")
    if col_del.button("RÉINITIALISER LA BASE DE DONNÉES"):
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
            st.warning("Base de données locale supprimée. L'application va redémarrer.")
            # st.rerun()

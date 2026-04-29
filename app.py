import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# --- 1. CONFIGURATION PRESTIGE ---
st.set_page_config(page_title="CUNI_VALENCE PRESTIGE", layout="wide")

# --- 2. DESIGN : INJECTION CSS AVANCÉE ---
st.markdown("""
<style>
    /* Fond sombre absolu */
    [data-testid="stAppViewContainer"] {
        background-color: #060606;
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }
    
    /* Menu Latéral */
    [data-testid="stSidebar"] {
        background-color: #0A0A0A;
        border-right: 1px solid #1A1A1A;
    }

    /* Titre style "DATA VALENCE" */
    .hero-title {
        font-size: 4rem;
        font-weight: 900;
        text-align: left;
        letter-spacing: -3px;
        line-height: 0.9;
        margin-bottom: 5px;
        color: #FFFFFF;
    }
    .teal-glow {
        color: #00FBFF;
        text-shadow: 0px 0px 15px rgba(0, 251, 255, 0.4);
    }

    /* Bandeau de Recherche Académique */
    .academic-module {
        font-size: 0.8rem;
        color: #00FBFF;
        background-color: rgba(0, 251, 255, 0.05);
        padding: 10px 15px;
        border-left: 3px solid #00FBFF;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 40px;
    }

    /* Cartes de statistiques */
    .stat-card {
        background-color: #111111;
        border: 1px solid #222;
        padding: 20px;
        border-radius: 4px;
        text-align: center;
    }

    /* Styliser les onglets */
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] {
        font-size: 1rem;
        font-weight: bold;
        color: #666;
    }
    .stTabs [aria-selected="true"] {
        color: #00FBFF !important;
        border-bottom: 2px solid #00FBFF !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. BACKEND : MOTEUR DE DONNÉES ROBUSTE ---
DB_FILE = "cuni_valence_database.csv"

def get_db():
    if os.path.exists(DB_FILE):
        try:
            data = pd.read_csv(DB_FILE)
            data['Date'] = data['Date'].astype(str) # Force format texte pour éviter bug ValueErr
            return data
        except:
            return pd.DataFrame(columns=["Date", "Secteur", "Variable", "Valeur", "Note"])
    return pd.DataFrame(columns=["Date", "Secteur", "Variable", "Valeur", "Note"])

df = get_db()

# --- 4. HEADER ---
st.markdown('<div class="hero-title">CUNI<span class="teal-glow">VALENCE</span></div>', unsafe_allow_html=True)
st.markdown('<div class="academic-module">ACADEMIC RESEARCH MODULE V1.2 // INF232 DATA ANALYSIS</div>', unsafe_allow_html=True)

# --- 5. NAVIGATION ---
st.sidebar.markdown("### SYSTEM COMMAND")
menu = st.sidebar.radio("MODULE SELECTOR", 
    ["1. START COLLECTION", "2. ANALYTICS DASHBOARD", "3. ARCHIVE & EXPORT"])

# --- MODULE 1 : COLLECTE (Intégrant tes 6 objectifs) ---
if menu == "1. START COLLECTION":
    st.subheader("CENTRE D'ACQUISITION MULTI-SECTEURS")
    
    with st.form("main_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            date_entry = st.date_input("DATE D'OBSERVATION")
            secteur = st.selectbox("OBJECTIF D'ANALYSE", [
                "SUIVI DE PRODUCTION (Croissance)",
                "SUIVI SANITAIRE (Santé/Mortalité)",
                "ALIMENTATION (Consommation/Coûts)",
                "REPRODUCTION (Cycles/Portées)",
                "ENVIRONNEMENT (Temp/Humidité)",
                "TRAÇABILITÉ (Mouvements)"
            ])
        
        with col2:
            variable = st.text_input("DÉSIGNATION (Ex: Poids Lot A, Temp Bureau, etc.)")
            valeur = st.number_input("MESURE NUMÉRIQUE", step=0.01)
        
        note = st.text_area("NOTES COMPLÉMENTAIRES")
        
        if st.form_submit_button("VALIDER L'ENTRÉE DANS LE CORE"):
            new_row = pd.DataFrame({
                "Date": [str(date_entry)],
                "Secteur": [secteur],
                "Variable": [variable],
                "Valeur": [float(valeur)],
                "Note": [note]
            })
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success("DATA SYNCHRONIZED SUCCESSFULLY.")
            st.rerun()

# --- MODULE 2 : ANALYTICS (Dashboard attractif) ---
elif menu == "2. ANALYTICS DASHBOARD":
    if not df.empty:
        st.subheader("VISUALISATION DES FLUX PRÉDICTIFS")
        
        # Stat Tiles
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("RELEVÉS TOTAL", len(df))
        c2.metric("VALEUR MOYENNE", f"{df['Valeur'].mean():.2f}")
        c3.metric("MAX RECORD", f"{df['Valeur'].max():.2f}")
        c4.metric("SECTEURS ACTIFS", df['Secteur'].nunique())

        st.markdown("---")
        
        # Graphique High-End
        tab_graph, tab_table = st.tabs(["DISTRIBUTION ANALYTIQUE", "SÉQUENCE DE DONNÉES"])
        
        with tab_graph:
            fig = px.violin(df, x="Secteur", y="Valeur", color="Secteur", box=True, points="all",
                            title="ANALYSE DE VARIANCE PAR SECTEUR OPÉRATIONNEL")
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#00FBFF")
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with tab_table:
            st.dataframe(df, use_container_width=True)
    else:
        st.info("SYSTEM IDLE: PLEASE INJECT DATA VIA COLLECTION MODULE.")

# --- MODULE 3 : ARCHIVE & EXPORT (Norme TP) ---
else:
    st.subheader("GESTION DE LA PERSISTENCE")
    st.write("Ce module assure la **Fiabilité** et la **Traçabilité** des données pour l'évaluation INF232.")
    
    if not df.empty:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="GÉNÉRER LE RAPPORT STRUCTUREL (.CSV)",
            data=csv,
            file_name=f"cuni_valence_export_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
        
        st.markdown("---")
        if st.button("RÉINITIALISER LA BASE DE DONNÉES"):
            if os.path.exists(DB_FILE):
                os.remove(DB_FILE)
                st.warning("DATABASE PURGED.")
                st.rerun()
    else:
        st.error("NO DATA AVAILABLE FOR EXPORT.")

# Sidebar Footer
st.sidebar.markdown("---")
st.sidebar.write("**VERSION:** 1.2.0-PRESTIGE")
st.sidebar.write("**STATUS:** NOMINAL ")
st.sidebar.write("**UY1 - INF 232**")       

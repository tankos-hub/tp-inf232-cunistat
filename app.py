import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Configuration de la page
st.set_page_config(page_title="CUNI VALENCE - INF232", layout="centered")

# 2. HACK CSS (Design sombre "Data Valence")
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    .main-title {
        font-size: 3.5rem;
        font-weight: 850;
        text-align: center;
        letter-spacing: -2px;
        color: #ffffff;
        margin-bottom: 0px;
    }
    .accent { color: #00FBFF; }
    .description-box {
        font-size: 0.9rem;
        text-align: center;
        color: #00FBFF;
        background-color: rgba(0, 251, 255, 0.1);
        padding: 12px;
        border: 1px solid rgba(0, 251, 255, 0.3);
        border-radius: 4px;
        margin-top: 15px;
        margin-bottom: 30px;
        text-transform: uppercase;
    }
    .stTabs [data-baseweb="tab-list"] { justify-content: center; }
    .stTabs [aria-selected="true"] {
        background-color: #00FBFF !important;
        color: #000000 !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 3. HEADER
st.markdown('<div class="main-title">CUNI <span class="accent">VALENCE</span></div>', unsafe_allow_html=True)
st.markdown('<div class="description-box">COLLECTE ET ANALYSE DESCRIPTIVE DE LA CROISSANCE ET DES FLUX PRODUCTIFS CUNICOLES.</div>', unsafe_allow_html=True)

# 4. GESTION DES DONNÉES
DB_FILE = "cunistat_data.csv"

def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["Date", "Stade", "Poids"])

def save_data(data_frame):
    data_frame.to_csv(DB_FILE, index=False)

df = load_data()

# 5. NAVIGATION
tab1, tab2 = st.tabs(["START COLLECTION", "OPEN DASHBOARD"])

with tab1:
    st.subheader("Enregistrement des mesures")
    with st.form("collection_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        date_val = c1.date_input("Date du relevé")
        stade_val = c1.selectbox("Stade de l'animal", ["Maternité", "Sevrage", "Engraissement", "Reproducteur"])
        poids_val = c2.number_input("Masse (kg)", min_value=0.01, step=0.01)
        
        submit_btn = st.form_submit_button("VALIDER L'ENREGISTREMENT")
        
        if submit_btn:
            new_row = pd.DataFrame([[str(date_val), stade_val, poids_val]], columns=["Date", "Stade", "Poids"])
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            st.success("Donnée synchronisée avec le module local.")
            st.rerun()

with tab2:
    st.subheader("Analyse Descriptive des Performances")
    if not df.empty:
        df["Poids"] = pd.to_numeric(df["Poids"])
        
        # Indicateurs
        m1, m2, m3 = st.columns(3)
        m1.metric("SUJETS (N)", len(df))
        m2.metric("MOYENNE (KG)", f"{df['Poids'].mean():.2f}")
        m3.metric("ÉCART-TYPE", f"{df['Poids'].std():.2f}")

        # Graphique
        fig = px.violin(df, y="Poids", x="Stade", color="Stade", box=True, points="all")
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        
        # --- SECTION EXPORTATION (Bouton Télécharger) ---
        st.markdown("---")
        st.write("### 📂 Gestion de la Base de Données")
        
        col_exp, col_del = st.columns(2)
        
        # Bouton Télécharger
        csv_data = df.to_csv(index=False).encode('utf-8')
        col_exp.download_button(
            label="📥 EXPORTER EN CSV",
            data=csv_data,
            file_name="cuni_valence_export.csv",
            mime="text/csv",
            help="Télécharger les données pour Excel ou une analyse externe"
        )
        
        # Bouton Réinitialiser (optionnel)
        if col_del.button("🗑️ VIDER LA BASE"):
            if os.path.exists(DB_FILE):
                os.remove(DB_FILE)
                st.rerun()
                
        with st.expander("Voir les données brutes"):
            st.dataframe(df, use_container_width=True)
    else:
        st.warning("Module d'analyse vide. Veuillez enregistrer des mesures.")

# Sidebar info
st.sidebar.markdown("### Info Projet")
st.sidebar.info("Application de suivi cunicole développée pour l'évaluation INF232 (UY1).")    

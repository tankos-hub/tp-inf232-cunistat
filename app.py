import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Configuration de la page
st.set_page_config(page_title="CUNI VALENCE - INF232", layout="centered")

# 2. HACK CSS (Le design sombre et moderne de ton ami)
st.markdown("""
<style>
    /* Fond sombre global */
    [data-testid="stAppViewContainer"] {
        background-color: #0E1117;
        color: #FFFFFF;
    }

    /* Titre principal style "DATA VALENCE" */
    .main-title {
        font-size: 3.5rem;
        font-weight: 850;
        text-align: center;
        letter-spacing: -2px;
        color: #ffffff;
        margin-bottom: 0px;
        font-family: 'Inter', sans-serif;
    }
    .accent {
        color: #00FBFF; /* Cyan néon */
    }

    /* Bandeau de description */
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
        letter-spacing: 1px;
    }

    /* Personnalisation des onglets (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #1A1C24;
        border-radius: 4px;
        color: white;
        padding: 10px 30px;
    }
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
st.caption("Filière Informatique L2 - UY1 | Module de Recherche Académique v1.0")

# 4. GESTION DES DONNÉES (CSV Local)
DB_FILE = "cunistat_data.csv"

def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["Date", "Stade", "Poids"])

def save_data(data_frame):
    data_frame.to_csv(DB_FILE, index=False)

df = load_data()

# 5. NAVIGATION PAR ONGLET (Comme sur l'image)
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
        
        # Métriques style Dashboard
        m1, m2, m3 = st.columns(3)
        m1.metric("SUJETS (N)", len(df))
        m2.metric("MOYENNE (KG)", f"{df['Poids'].mean():.2f}")
        m3.metric("ÉCART-TYPE", f"{df['Poids'].std():.2f}")

        # Graphique avancé (Violin Plot pour l'analyse de distribution)
        fig = px.violin(df, y="Poids", x="Stade", color="Stade", box=True, points="all",
                        title="Distribution des masses par catégorie")
        
        # Thème sombre pour le graphique
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("Consulter l'historique complet"):
            st.dataframe(df, use_container_width=True)
            
            # Option de téléchargement pour le prof
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button("EXPORTER LES DONNÉES (.CSV)", csv_data, "data_cunistat.csv", "text/csv")
    else:
        st.warning("Module d'analyse en attente de données. Veuillez utiliser l'onglet COLLECTION.")

# Footer informatif
st.sidebar.markdown("---")
st.sidebar.write("**Étudiant :** [Ton Nom]")
st.sidebar.write("**Cours :** INF 232 - Analyse de données")
st.sidebar.write("**Serveur :** Opérationnel ✅")

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px

# Configuration Académique
st.set_page_config(page_title="INF232 - Analyse de Données", layout="wide")

st.title("Plateforme de Collecte et d'Analyse Descriptive")
st.subheader("Secteur : AgriTech (Cuniculture)")

# --- CONNEXION PERMANENTE ---
# Remplace l'URL ci-dessous par celle de ton Google Sheets
URL_SHEET = "TON_LIEN_GOOGLE_SHEETS_ICI"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=URL_SHEET)
except:
    df = pd.DataFrame(columns=["Date", "Stade", "Poids"])

# --- INTERFACE ---
menu = st.sidebar.selectbox("Menu Principal", ["Collecte de données", "Dashboard Statistique", "Informations"])

if menu == "Collecte de données":
    st.info("Formulaire d'enregistrement des pesées hebdomadaires")
    with st.form("input_form"):
        c1, c2 = st.columns(2)
        date_obs = c1.date_input("Date du relevé")
        stade_obs = c1.selectbox("Stade de croissance", ["Maternité", "Engraissement", "Reproduction"])
        poids_obs = c2.number_input("Masse mesurée (kg)", min_value=0.01, step=0.01)
        
        btn = st.form_submit_button("Enregistrer dans le Cloud")
        
        if btn:
            new_entry = pd.DataFrame([[str(date_obs), stade_obs, poids_obs]], columns=["Date", "Stade", "Poids"])
            updated_df = pd.concat([df, new_entry], ignore_index=True)
            conn.update(spreadsheet=URL_SHEET, data=updated_df)
            st.success("Donnée sécurisée dans Google Sheets !")
            st.balloons()

elif menu == "Dashboard Statistique":
    if not df.empty:
        df["Poids"] = pd.to_numeric(df["Poids"])
        
        # 1. Indicateurs descriptifs
        st.markdown("### 📈 Statistiques Globales")
        col1, col2, col3 = st.columns(3)
        col1.metric("Effectif (n)", len(df))
        col2.metric("Moyenne", f"{df['Poids'].mean():.3f} kg")
        col3.metric("Variance", f"{df['Poids'].var():.4e}")

        # 2. Visualisation (Analyse par groupe)
        st.markdown("### 📊 Répartition par Stade")
        fig = px.violin(df, y="Poids", x="Stade", box=True, points="all", color="Stade")
        st.plotly_chart(fig, use_container_width=True)
        
        # 3. Tableau de données
        with st.expander("Consulter la base de données brute"):
            st.dataframe(df, use_container_width=True)
    else:
        st.warning("Base de données vide. Enregistrez des mesures pour voir l'analyse.")

else:
    st.write("**Étudiant :** Votre Nom")
    st.write("**Filière :** Informatique L2 - UY1")
    st.write("**Cours :** INF 232 EC2 - Analyse de données")

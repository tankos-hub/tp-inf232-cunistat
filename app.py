import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuration académique sobre
st.set_page_config(page_title="INF232 - Analyse de Données", layout="wide")

st.title("Système de Collecte et d'Analyse Cunicole")
st.caption("Filière Informatique - UY1 | INF 232 EC2")

# --- GESTION DE LA BASE DE DONNÉES (LOCALE) ---
DB_FILE = "database_collecte.csv"

def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["Date", "Stade", "Poids"])

def save_data(df):
    df.to_csv(DB_FILE, index=False)

# Chargement des données
df = load_data()

# --- INTERFACE ---
st.sidebar.header("Navigation")
menu = st.sidebar.radio("Aller vers :", ["Collecte de données", "Tableau de bord Statistique", "Gestion du fichier"])

if menu == "Collecte de données":
    st.subheader("Formulaire d'enregistrement")
    with st.form("input_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        date_obs = col1.date_input("Date du relevé")
        stade_obs = col1.selectbox("Stade de croissance", ["Maternité", "Engraissement", "Reproduction"])
        poids_obs = col2.number_input("Masse mesurée (kg)", min_value=0.01, max_value=15.0, step=0.01)
        
        submit = st.form_submit_button("Enregistrer la donnée")
        
        if submit:
            new_entry = pd.DataFrame([[str(date_obs), stade_obs, poids_obs]], columns=["Date", "Stade", "Poids"])
            df = pd.concat([df, new_entry], ignore_index=True)
            save_data(df)
            st.success("Donnée enregistrée avec succès !")
            st.rerun()

elif menu == "Tableau de bord Statistique":
    st.subheader("Analyse Descriptive")
    if not df.empty:
        # Nettoyage rapide pour l'analyse
        df["Poids"] = pd.to_numeric(df["Poids"])
        
        # Indicateurs
        m1, m2, m3 = st.columns(3)
        m1.metric("Sujets mesurés", len(df))
        m2.metric("Moyenne (kg)", f"{df['Poids'].mean():.2f}")
        m3.metric("Écart-type", f"{df['Poids'].std():.2f}")

        # Graphique robuste
        st.markdown("### Distribution des masses par stade")
        fig = px.box(df, x="Stade", y="Poids", color="Stade", points="all")
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Aucune donnée disponible. Commencez par la collecte.")

else:
    st.subheader("Paramètres et Exportation")
    st.write("Pour valider le critère de **Fiabilité**, vous pouvez télécharger la base de données actuelle.")
    
    if not df.empty:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Télécharger le fichier .CSV", data=csv, file_name="data_inf232.csv", mime="text/csv")
    
    if st.button("Réinitialiser la base de données (Danger)"):
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
            st.warning("Base de données supprimée.")
            st.rerun()

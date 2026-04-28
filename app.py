import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration sobre
st.set_page_config(page_title="Analyse de données - INF232", layout="wide")

# Suppression des emojis pour un look plus pro
st.title("Système de Collecte et d'Analyse Cunicole")
st.caption("Projet INF 232 EC2 - Analyse de données descriptives")

# --- BACKEND : Gestion de la persistance (Simulée par fichier pour le TP) ---
# Note : Pour un vrai déploiement permanent, on utilise Google Sheets.
# Pour le TP, nous allons utiliser un fichier CSV local sur le serveur.
DB_FILE = "data_collecte.csv"

def load_data():
    try:
        return pd.read_csv(DB_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Stade", "Poids"])

def save_data(df):
    df.to_csv(DB_FILE, index=False)

# Chargement initial
df = load_data()

# --- INTERFACE ---
st.sidebar.header("Navigation")
menu = st.sidebar.radio("Aller vers :", ["Saisie des données", "Tableau de bord"])

if menu == "Saisie des données":
    st.subheader("Formulaire de collecte")
    with st.form("form_saisie", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Date du relevé")
            stade = st.selectbox("Phase d'élevage", ["Maternité", "Engraissement", "Reproduction"])
        with col2:
            poids = st.number_input("Poids mesuré (kg)", min_value=0.05, max_value=12.0, step=0.01)
        
        submit = st.form_submit_button("Valider l'enregistrement")
        
        if submit:
            new_data = pd.DataFrame([[date, stade, poids]], columns=["Date", "Stade", "Poids"])
            df = pd.concat([df, new_data], ignore_index=True)
            save_data(df)
            st.success("Donnée enregistrée avec succès dans la base.")

else:
    st.subheader("Analyse Descriptive des données")
    if not df.empty:
        # Indicateurs statistiques
        m1, m2, m3 = st.columns(3)
        m1.metric("Effectif total", len(df))
        m2.metric("Poids moyen", f"{df['Poids'].mean():.2f} kg")
        m3.metric("Ecart-type", f"{df['Poids'].std():.2f}")

        # Graphiques
        fig = px.box(df, x="Stade", y="Poids", title="Distribution des poids par stade")
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("### Historique des données")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("La base de données est vide. Veuillez effectuer des saisies.")

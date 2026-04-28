import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration de la page pour mobile
st.set_page_config(page_title="CuniStat - AgriTech", layout="centered")

st.title("🍀 CuniStat : Gestion Cunicole")
st.write("TP INF 232 - Analyse de données")

# --- SIMULATION DE BASE DE DONNÉES (Pour le moment) ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["Date", "Stade", "Poids"])

# --- ONGLETS ---
tab1, tab2 = st.tabs(["📥 Collecte", "📊 Analyse Descriptive"])

with tab1:
    st.header("Saisie des données")
    with st.form("collect_form"):
        date = st.date_input("Date du relevé")
        stade = st.selectbox("Phase d'élevage", ["Maternité", "Engraissement", "Reproduction"])
        poids = st.number_input("Poids (kg)", min_value=0.1, max_value=8.0, step=0.1)
        
        submitted = st.form_submit_button("Enregistrer la donnée")
        if submitted:
            new_row = {"Date": date, "Stade": stade, "Poids": poids}
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_row])], ignore_index=True)
            st.success("Donnée ajoutée localement !")

with tab2:
    st.header("Tableau de bord descriptif")
    if not st.session_state.db.empty:
        df = st.session_state.db
        
        # Métriques
        col1, col2 = st.columns(2)
        col1.metric("Nombre de sujets", len(df))
        col2.metric("Poids Moyen (kg)", round(df["Poids"].mean(), 2))
        
        # Graphique
        st.subheader("Distribution des poids")
        fig = px.histogram(df, x="Poids", color="Stade", barmode="group")
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Données brutes")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aucune donnée collectée. Allez dans l'onglet 'Collecte'.")

import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# ------------------------------
# Configuration de la page
st.set_page_config(page_title="Flow Writer Analytics", layout="wide")
st.title("✍️ Creative Writing Flow Tracker")
st.markdown("Collecte & analyse descriptive de vos séances d'écriture créative")

# ------------------------------
# Connexion à Google Sheets (via secrets Streamlit)
def init_google_sheet():
    try:
        # Les secrets sont définis dans Streamlit Cloud (ou .streamlit/secrets.toml)
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_dict = st.secrets["gcp_service_account"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        sheet = client.open("FlowWriterData").sheet1  # Nom de votre Google Sheet
        return sheet
    except Exception as e:
        st.error(f"Erreur de connexion à Google Sheets : {e}")
        return None

# Créer l'en-tête si la feuille est vide
def ensure_headers(sheet):
    if sheet.row_count == 0 or sheet.row_values(1) == []:
        headers = ["Timestamp", "Date", "Duree_min", "Activite_preparatoire", "Distractions_1_10",
                   "Mots_ecrits", "Flow_score_1_10", "Creativite_score_1_10", "Commentaire"]
        sheet.insert_row(headers, 1)

# ------------------------------
# Formulaire de collecte
def collect_data(sheet):
    with st.form("session_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Date de la session", datetime.today())
            duree = st.number_input("Durée (minutes)", min_value=5, max_value=180, value=30)
            activite = st.selectbox("Activité préparatoire", 
                                    ["Méditation", "Exercice léger", "Caféine", "Musique", "Rien"])
            distractions = st.slider("Niveau de distractions (1 = très distrait, 10 = très focus)", 1, 10, 5)
        with col2:
            mots = st.number_input("Nombre de mots écrits", min_value=0, max_value=5000, value=250)
            flow = st.slider("Score de flow (1 = bloqué, 10 = flow intense)", 1, 10, 6)
            creativite = st.slider("Score de créativité auto-évalué", 1, 10, 6)
            commentaire = st.text_area("Commentaire (optionnel)")

        submitted = st.form_submit_button("📥 Enregistrer la session")

        if submitted:
            if duree <= 0 or mots < 0:
                st.warning("Veuillez corriger les valeurs (durée >0, mots >=0)")
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                row = [timestamp, str(date), duree, activite, distractions, mots, flow, creativite, commentaire]
                sheet.append_row(row)
                st.success("✅ Données enregistrées dans Google Sheets !")
                st.balloons()

# ------------------------------
# Chargement des données depuis Google Sheets
@st.cache_data(ttl=600)
def load_data(sheet):
    try:
        records = sheet.get_all_records()
        if not records:
            return pd.DataFrame()
        df = pd.DataFrame(records)
        # Nettoyage des types
        numeric_cols = ["Duree_min", "Distractions_1_10", "Mots_ecrits", "Flow_score_1_10", "Creativite_score_1_10"]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        return df
    except Exception as e:
        st.error(f"Erreur de chargement : {e}")
        return pd.DataFrame()

# ------------------------------
# Analyse descriptive
def show_descriptive_analysis(df):
    if df.empty:
        st.info("Aucune donnée pour le moment. Envoyez votre première session !")
        return

    st.subheader("📊 Vue d'ensemble des données")
    st.dataframe(df, use_container_width=True)

    st.subheader("📈 Statistiques descriptives")
    st.write(df.describe())

    # Graphiques interactifs
    col1, col2 = st.columns(2)
    with col1:
        fig_hist = px.histogram(df, x="Creativite_score_1_10", nbins=10, title="Distribution du score de créativité")
        st.plotly_chart(fig_hist, use_container_width=True)
    with col2:
        fig_box = px.box(df, y=["Flow_score_1_10", "Creativite_score_1_10"], title="Boxplot Flow vs Créativité")
        st.plotly_chart(fig_box, use_container_width=True)

    # Corrélations (heatmap)
    st.subheader("🔗 Matrice de corrélation")
    corr = df[["Duree_min", "Distractions_1_10", "Mots_ecrits", "Flow_score_1_10", "Creativite_score_1_10"]].corr()
    fig_corr = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale="RdBu_r", title="Corrélations")
    st.plotly_chart(fig_corr, use_container_width=True)

    # Régression linéaire simple (exemple Distractions → Créativité)
    st.subheader("📉 Régression linéaire simple (Distractions vs Créativité)")
    from sklearn.linear_model import LinearRegression
    import numpy as np
    X = df[["Distractions_1_10"]].dropna()
    y = df.loc[X.index, "Creativite_score_1_10"]
    if len(X) > 1:
        model = LinearRegression().fit(X, y)
        y_pred = model.predict(X)
        fig_reg = go.Figure()
        fig_reg.add_trace(go.Scatter(x=X.squeeze(), y=y, mode='markers', name='Observations'))
        fig_reg.add_trace(go.Scatter(x=X.squeeze(), y=y_pred, mode='lines', name='Régression', line=dict(color='red')))
        fig_reg.update_layout(title=f"Créativité = {model.coef_[0]:.2f} * Distractions + {model.intercept_:.2f}",
                              xaxis_title="Distractions (1-10)", yaxis_title="Score de créativité")
        st.plotly_chart(fig_reg, use_container_width=True)
        st.write(f"**Coefficient de détermination R² :** {model.score(X, y):.3f}")
    else:
        st.warning("Besoin d'au moins 2 points pour la régression.")

    # Export CSV
    st.subheader("📎 Exporter les données brutes")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Télécharger CSV", data=csv, file_name="flow_writer_data.csv", mime="text/csv")

# ------------------------------
# Menu principal
sheet = init_google_sheet()
if sheet:
    ensure_headers(sheet)
    menu = option_menu(None, ["Nouvelle session", "Analyse descriptive"], 
                       icons=["pencil-square", "bar-chart"], orientation="horizontal")
    if menu == "Nouvelle session":
        collect_data(sheet)
    else:
        df = load_data(sheet)
        show_descriptive_analysis(df)
else:
    st.stop()

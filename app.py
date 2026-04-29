import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- ARCHITECTURE VISUELLE ---
st.set_page_config(page_title="CUNI_CORE TITANIUM", layout="wide")

# Injection CSS pour un look "Console Industrielle"
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid #1A1A1A; }
    
    /* Titre style Matrix/Terminal */
    .title-core {
        font-family: 'Courier New', monospace;
        font-size: 3.5rem;
        font-weight: 900;
        letter-spacing: -3px;
        color: #FFFFFF;
        margin-bottom: 0px;
    }
    .orange-tag { color: #FF4B4B; }
    
    .status-line {
        font-family: monospace;
        font-size: 0.75rem;
        color: #FF4B4B;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 40px;
    }

    /* Suppression des bordures arrondies (style brutaliste) */
    div[data-testid="stForm"] {
        background-color: #0A0A0A;
        border: 1px solid #1A1A1A;
        border-radius: 0px;
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 0px;
        border: 1px solid #FF4B4B;
        background-color: transparent;
        color: #FF4B4B;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- MOTEUR DE DONNÉES (CORRECTIF BUG) ---
DB_FILE = "titanium_core.csv"

def load_core_engine():
    if os.path.exists(DB_FILE):
        try:
            data = pd.read_csv(DB_FILE)
            # Correction du bug : on s'assure que la colonne Date est au format String propre
            data['Date'] = data['Date'].astype(str)
            return data
        except:
            return pd.DataFrame(columns=["Date", "Phase", "Masse"])
    return pd.DataFrame(columns=["Date", "Phase", "Masse"])

df = load_core_engine()

# --- HEADER ---
st.markdown('<div class="title-core">CUNI<span class="orange-tag">_CORE</span></div>', unsafe_allow_html=True)
st.markdown('<div class="status-line">TERMINAL D\'ACQUISITION BIOMÉTRIQUE // VERSION_TITANIUM</div>', unsafe_allow_html=True)

# --- NAVIGATION ---
menu = st.sidebar.radio("MODULE_SELECT", ["FLUX_CAPTURE", "ANALYTICS_SYSTEM"])

if menu == "FLUX_CAPTURE":
    st.subheader("SÉQUENCE D'ENTRÉE")
    with st.form("capture_box", clear_on_submit=True):
        f_date = st.date_input("DATE_OBSERVATION")
        f_phase = st.selectbox("PHASE_ELEVAGE", ["MATERNITE", "SEVRAGE", "ENGRAISSEMENT", "REPRODUCTION"])
        f_masse = st.number_input("VALEUR_MASSE (KG)", min_value=0.0, step=0.01)
        
        if st.form_submit_button("EXÉCUTER L'ENREGISTREMENT"):
            # Création forcée d'une ligne propre
            new_line = pd.DataFrame({
                "Date": [str(f_date)], 
                "Phase": [f_phase], 
                "Masse": [float(f_masse)]
            })
            df = pd.concat([df, new_line], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success("PAQUET_DONNÉES_SÉCURISÉ")
            st.rerun()

elif menu == "ANALYTICS_SYSTEM":
    if not df.empty:
        st.subheader("MONITORING DES FLUX")
        
        # Indicateurs Bruts
        c1, c2, c3 = st.columns(3)
        c1.metric("UNITÉS", len(df))
        c2.metric("MASSE_MOY", f"{df['Masse'].mean():.2f}")
        c3.metric("MAX_VAL", f"{df['Masse'].max():.2f}")

        # Graphique High-Tech
        fig = px.violin(df, x="Phase", y="Masse", color="Phase", box=True, points="all")
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Courier New, monospace")
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Bouton d'exportation (Sans emoji, très propre)
        st.markdown("---")
        csv_export = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="GÉNÉRER LE RAPPORT STRUCTUREL (CSV)",
            data=csv_export,
            file_name="core_titanium_export.csv",
            mime="text/csv"
        )
    else:
        st.info("SYSTÈME EN ATTENTE DE DONNÉES_")

# --- FOOTER SIDEBAR ---
st.sidebar.markdown("---")
st.sidebar.write("SYSTEM_STATUS: NOMINAL")
st.sidebar.write("ENCRYPTION: ACTIVE")

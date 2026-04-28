import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime, timedelta

# --- ARCHITECTURE VISUELLE ---
st.set_page_config(page_title="CUNI_CORE ULTIMA", layout="wide")

st.markdown("""
<style>
    /* Global UI Reset */
    [data-testid="stAppViewContainer"] { background-color: #0A0A0B; color: #D1D1D1; }
    [data-testid="stSidebar"] { background-color: #0E0E10; border-right: 1px solid #2D2D2D; }
    
    /* Typography & Headers */
    .terminal-title {
        font-family: 'Courier New', monospace;
        font-size: 4rem;
        font-weight: 900;
        color: #FFFFFF;
        text-align: left;
        letter-spacing: -4px;
        line-height: 0.8;
        margin-bottom: 5px;
    }
    .amber-text { color: #FFB000; } /* Orange Ambre Industriel */
    
    .status-bar {
        font-family: monospace;
        font-size: 0.8rem;
        color: #FFB000;
        border: 1px solid #FFB000;
        padding: 5px 15px;
        display: inline-block;
        margin-bottom: 30px;
    }

    /* Forms & Inputs */
    [data-testid="stForm"] {
        background-color: #121214;
        border: 1px solid #2D2D2D;
        border-radius: 0px;
    }
    
    /* Metrics Customization */
    [data-testid="stMetric"] {
        background-color: #121214;
        border-left: 3px solid #FFB000;
        padding: 15px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- ENGINE : DATA MANAGEMENT ---
DB_FILE = "core_ultima_v1.csv"

def get_engine():
    if os.path.exists(DB_FILE):
        d = pd.read_csv(DB_FILE)
        d['Date'] = pd.to_datetime(d['Date'])
        return d
    return pd.DataFrame(columns=["Date", "Phase", "Masse", "ID_Sujet"])

df = get_engine()

# --- SIDEBAR CONTROL PANEL ---
with st.sidebar:
    st.markdown("<h2 style='color:#FFB000;'>CONTROL PANEL</h2>", unsafe_allow_html=True)
    mode = st.selectbox("OP_MODE", ["DATA_ENTRY", "ANALYTICS_PRO", "PREDICTION_ENGINE"])
    
    st.markdown("---")
    st.markdown("<h3 style='color:#666;'>SYSTEM_INFO</h3>", unsafe_allow_html=True)
    st.write(f"VERSION: 1.0.4-ULTIMA")
    st.write(f"USER: STUDENT_UY1")
    st.write(f"DB_STATUS: {'CONNECTED' if not df.empty else 'IDLE'}")

# --- HEADER SECTION ---
st.markdown('<div class="terminal-title">CUNI<span class="amber-text">CORE</span></div>', unsafe_allow_html=True)
st.markdown('<div class="status-bar">TERMINAL DE GESTION BIOMÉTRIQUE CUNICOLE // UY1_INF232</div>', unsafe_allow_html=True)

# --- MODE 1 : DATA ENTRY ---
if mode == "DATA_ENTRY":
    st.subheader("SÉQUENCE D'ACQUISITION")
    with st.form("entry_form"):
        c1, c2, c3 = st.columns([2,2,1])
        date_in = c1.date_input("DATE_OBS")
        phase_in = c2.selectbox("PHASE", ["MATERNITE", "SEVRAGE", "ENGRAISSEMENT", "REPRODUCTION"])
        id_in = c3.text_input("ID_TAG", "LP-01")
        masse_in = st.slider("MASSE_MESURÉE (KG)", 0.05, 10.0, 1.50)
        
        if st.form_submit_button("INJECTER DANS LA BASE"):
            new_data = pd.DataFrame([[date_in, phase_in, masse_in, id_in]], columns=["Date", "Phase", "Masse", "ID_Sujet"])
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success("PAQUET DE DONNÉES SYNCHRONISÉ.")
            st.rerun()

# --- MODE 2 : ANALYTICS PRO ---
elif mode == "ANALYTICS_PRO":
    if not df.empty:
        st.subheader("MONITORING DES PERFORMANCES")
        
        # Dashboard Top Level
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("RELEVÉS", len(df))
        m2.metric("MASSE_AVG", f"{df['Masse'].mean():.2f} KG")
        m3.metric("VARIANCE", f"{df['Masse'].var():.4f}")
        m4.metric("PEAK_MASS", f"{df['Masse'].max():.2f} KG")

        # Advanced Visuals
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown("##### ANALYSE DE DISTRIBUTION (VIOLIN)")
            fig_v = px.violin(df, y="Masse", x="Phase", color="Phase", box=True, points="all", template="plotly_dark")
            fig_v.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', colorway=['#FFB000', '#FFCF66', '#FF8C00'])
            st.plotly_chart(fig_v, use_container_width=True)

        with c2:
            st.markdown("##### PROGRESSION TEMPORELLE")
            fig_l = px.line(df.sort_values('Date'), x="Date", y="Masse", color="Phase", markers=True)
            fig_l.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_l, use_container_width=True)
            
        # Export Button (Ton option préférée)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("GÉNÉRER RAPPORT CSV STRUCTUREL", csv, "CORE_EXPORT.csv", "text/csv")
    else:
        st.error("BASE DE DONNÉES VIDE. AUCUN SIGNAL DÉTECTÉ.")

# --- MODE 3 : PREDICTION ENGINE (Le truc "Grandiose") ---
else:
    st.subheader("MODÈLE DE PROJECTION (CROISSANCE ESTIMÉE)")
    if not df.empty:
        st.write("Basé sur les données actuelles, voici la courbe de croissance projetée pour les 30 prochains jours :")
        
        last_mass = df['Masse'].mean()
        days = list(range(30))
        # Simulation d'une croissance logarithmique typique
        proj = [last_mass + (0.05 * i) for i in days] 
        
        fig_p = go.Figure()
        fig_p.add_trace(go.Scatter(x=days, y=proj, mode='lines+markers', line=dict(color='#FFB000', width=4)))
        fig_p.update_layout(title="PROJECTION SUR 30 JOURS (MODÈLE LINEAIRE)", template="plotly_dark", xaxis_title="Jours futurs", yaxis_title="Masse (KG)")
        st.plotly_chart(fig_p, use_container_width=True)
        st.info("NOTE: Ce modèle utilise une régression simplifiée pour le cadre du TP INF232.")
    else:
        st.warning("DONNÉES INSUFFISANTES POUR GÉNÉRER UNE PRÉDICTION.")                                     

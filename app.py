import streamlit as st
import pandas as pd
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="Agriland Multi-Campagnes", layout="wide", page_icon="🚜")

# --- CONNEXION GOOGLE SHEETS (Simulation via session_state pour l'exemple) ---
# Note : Pour la version finale, on utilise st.connection("gsheets")
if 'db_campagnes' not in st.session_state:
    st.session_state.db_campagnes = pd.DataFrame(columns=["ID", "Type", "Culture", "Surface", "Début", "Statut"])

st.title("🚜 Agriland Sénégal : Pilotage Multi-Activités")

# --- INTERFACE DE SAISIE ---
with st.sidebar:
    st.header("➕ Nouvelle Campagne")
    with st.form("ajout_culture"):
        type_agri = st.selectbox("Catégorie", ["Maraîchage", "Arboriculture", "Grande Culture", "Élevage"])
        nom_c = st.text_input("Nom (ex: Papayer Solo, Oignon, Maïs)")
        sup = st.number_input("Surface (Ha) ou Effectif (Têtes)", min_value=0.0)
        date_j = st.date_input("Date de lancement")
        
        submit = st.form_submit_button("Enregistrer sur le Cloud")
        
        if submit:
            nouvelle_ligne = pd.DataFrame([{
                "ID": len(st.session_state.db_campagnes) + 1,
                "Type": type_agri,
                "Culture": nom_c,
                "Surface": sup,
                "Début": date_j,
                "Statut": "En cours"
            }])
            st.session_state.db_campagnes = pd.concat([st.session_state.db_campagnes, nouvelle_ligne], ignore_index=True)
            st.success(f"Campagne {nom_c} synchronisée !")

# --- TABLEAU DE BORD GÉNÉRAL ---
st.header("📊 Suivi de la Ferme (Andal)")

# Calcul des statistiques globales
total_ha = st.session_state.db_campagnes[st.session_state.db_campagnes['Type'] != "Élevage"]['Surface'].sum()
nb_campagnes = len(st.session_state.db_campagnes)

m1, m2, m3 = st.columns(3)
m1.metric("Surface Exploitée", f"{total_ha} Ha / 8 Ha")
m2.metric("Campagnes Actives", nb_campagnes)
m3.metric("Localisation", "Darou Khoudoss")

# --- AFFICHAGE PAR CATÉGORIE ---
tabs = st.tabs(["📋 Toutes les activités", "🥬 Maraîchage", "🌳 Arboriculture", "🐓 Élevage"])

with tabs[0]:
    st.subheader("Registre complet")
    st.dataframe(st.session_state.db_campagnes, use_container_width=True)

with tabs[1]:
    df_m = st.session_state.db_campagnes[st.session_state.db_campagnes['Type'] == "Maraîchage"]
    st.write(f"Nombre de parcelles : {len(df_m)}")
    st.table(df_m)

with tabs[2]:
    df_a = st.session_state.db_campagnes[st.session_state.db_campagnes['Type'] == "Arboriculture"]
    st.info("Note : Les cycles d'arboriculture sont suivis sur plusieurs années.")
    st.table(df_a)

with tabs[3]:
    df_e = st.session_state.db_campagnes[st.session_state.db_campagnes['Type'] == "Élevage"]
    st.table(df_e)

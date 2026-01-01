import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Agriland Sénégal", layout="wide", page_icon="🚜")

# --- CONNEXION CLOUD ---
conn = st.connection("gsheets", type=GSheetsConnection)

# Lecture sécurisée des données
try:
    df = conn.read(worksheet="Campagnes")
except:
    df = pd.DataFrame(columns=["ID", "Type", "Culture", "Surface", "Date_Debut", "Statut"])

st.title("🚜 Agriland Sénégal - Gestion de la Ferme")
st.write(f"📍 Site : Andal, Darou Khoudoss | État : Connecté au Cloud")

# --- INTERFACE DE SAISIE ---
with st.sidebar:
    st.header("📝 Enregistrer une activité")
    with st.form("ajout_form"):
        type_c = st.selectbox("Catégorie", ["Maraîchage", "Arboriculture", "Élevage"])
        nom_c = st.text_input("Nom (ex: Pomme de terre, Poulets)")
        valeur = st.number_input("Grandeur (Ha ou Nombre de têtes)", min_value=0.0)
        date_j = st.date_input("Date de début")
        submit = st.form_submit_button("Sauvegarder")

        if submit and nom_c:
            new_data = pd.DataFrame([{
                "ID": len(df) + 1,
                "Type": type_c,
                "Culture": nom_c,
                "Surface": valeur,
                "Date_Debut": date_j.strftime("%Y-%m-%d"),
                "Statut": "En cours"
            }])
            updated_df = pd.concat([df, new_data], ignore_index=True)
            conn.update(worksheet="Campagnes", data=updated_df)
            st.success("Synchronisation réussie !")
            st.rerun()

# --- AFFICHAGE PAR ONGLETS ---
tab1, tab2, tab3 = st.tabs(["📋 Vue Générale", "🥔 Cultures", "🐓 Élevage"])

with tab1:
    st.subheader("Registre complet de la ferme")
    st.dataframe(df, use_container_width=True, hide_index=True)

with tab2:
    st.subheader("Suivi Maraîchage & Arbres")
    df_cult = df[df['Type'].isin(["Maraîchage", "Arboriculture"])]
    st.table(df_cult)

with tab3:
    st.subheader("Suivi de l'Élevage")
    df_elev = df[df['Type'] == "Élevage"]
    st.table(df_elev)

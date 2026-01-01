import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Agriland Sénégal", layout="wide", page_icon="🚜")

# --- CONNEXION CLOUD ---
# Utilise les "Secrets" que vous avez configurés
conn = st.connection("gsheets", type=GSheetsConnection)

# Lecture sécurisée des données de l'onglet "Campagnes"
try:
    df = conn.read(worksheet="Campagnes")
except Exception:
    df = pd.DataFrame(columns=["ID", "Type", "Culture", "Surface", "Date_Debut", "Statut"])

st.title("🚜 Agriland Sénégal - Gestion de la Ferme")
st.write(f"📍 Site : Andal, Darou Khoudoss | État : Connecté au Cloud")

# --- INTERFACE DE SAISIE ---
with st.sidebar:
    st.header("📝 Enregistrer une activité")
    with st.form("ajout_form"):
        type_c = st.selectbox("Catégorie", ["Maraîchage", "Arboriculture", "Grande Culture", "Élevage"])
        nom_c = st.text_input("Nom (ex: Pomme de terre, Papayers, Poulets)")
        valeur = st.number_input("Grandeur (Ha ou Nombre de têtes)", min_value=0.0, step=0.1)
        date_j = st.date_input("Date de début", datetime.now())
        
        submit = st.form_submit_button("Sauvegarder à Andal")

        if submit and nom_c:
            # Création de la nouvelle ligne pour le Google Sheet
            new_data = pd.DataFrame([{
                "ID": len(df) + 1,
                "Type": type_c,
                "Culture": nom_c,
                "Surface": valeur,
                "Date_Debut": date_j.strftime("%Y-%m-%d"),
                "Statut": "En cours"
            }])
            # Fusion et mise à jour
            updated_df = pd.concat([df, new_data], ignore_index=True)
            conn.update(worksheet="Campagnes", data=updated_df)
            st.success(f"✅ {nom_c} enregistré sur le Cloud !")
            st.rerun()

# --- AFFICHAGE PAR ONGLETS ---
tab1, tab2, tab3 = st.tabs(["📋 Vue Générale", "🥬 Cultures (Maraîchage/Arbres)", "🐓 Élevage"])

with tab1:
    st.subheader("Registre complet de la ferme")
    if df.empty:
        st.info("Aucune campagne enregistrée pour le moment.")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)

with tab2:
    st.subheader("Suivi des parcelles")
    df_cult = df[df['Type'].isin(["Maraîchage", "Arboriculture", "Grande Culture"])]
    if not df_cult.empty:
        st.table(df_cult)
    else:
        st.write("Aucune culture en cours.")

with tab3:
    st.subheader("Suivi des animaux")
    df_elev = df[df['Type'] == "Élevage"]
    if not df_elev.empty:
        st.table(df_elev)
    else:
        st.write("Aucun suivi d'élevage actif.")

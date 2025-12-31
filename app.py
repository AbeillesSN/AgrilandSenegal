import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Agriland Cloud", layout="wide")

st.title("🚜 Agriland Sénégal - Synchronisation Cloud")

# Connexion réelle au Google Sheet
conn = st.connection("gsheets", type=GSheetsConnection)

# Lecture des données existantes
df = conn.read(ttl="10m") # Garde les données en mémoire 10 min

with st.sidebar:
    st.header("🌿 Ajouter une Culture")
    with st.form("form_agriland"):
        type_c = st.selectbox("Type", ["Arboriculture", "Maraîchage", "Élevage"])
        nom_c = st.text_input("Nom de la culture/espèce")
        surf = st.number_input("Grandeur (Ha ou Têtes)", min_value=0.0)
        submit = st.form_submit_button("Sauvegarder à Andal")

        if submit:
            # Création de la nouvelle ligne
            new_data = pd.DataFrame([{"Type": type_c, "Nom": nom_c, "Valeur": surf}])
            # Fusion avec l'ancien tableau
            updated_df = pd.concat([df, new_data], ignore_index=True)
            # Mise à jour du Google Sheet
            conn.update(spreadsheet=st.secrets["connections"]["gsheets"]["spreadsheet"], data=updated_df)
            st.success("Données envoyées sur Google Sheets !")

st.header("📊 État actuel de la Ferme")
st.dataframe(df, use_container_width=True)

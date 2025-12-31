import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="Agriland Sénégal - Gestion", layout="wide", page_icon="🚜")

st.title("🚜 Agriland Sénégal - Gestion de la Ferme")
st.info("📍 Darou Khoudoss, Andal | Connexion Cloud Active")

# --- CONNEXION AU GOOGLE SHEET ---
# Utilise la configuration 'gsheets' définie dans vos Secrets Streamlit
conn = st.connection("gsheets", type=GSheetsConnection)

# Lecture des données existantes dans l'onglet "Campagnes"
try:
    df = conn.read(worksheet="Campagnes")
except Exception:
    # Si l'onglet est vide, on crée une structure de base
    df = pd.DataFrame(columns=["ID", "Type", "Culture", "Surface", "Date_Debut", "Statut"])

# --- INTERFACE DE SAISIE (Barre latérale) ---
with st.sidebar:
    st.header("➕ Nouvelle Campagne")
    with st.form("form_ajout"):
        type_c = st.selectbox("Catégorie", ["Maraîchage", "Arboriculture", "Grande Culture", "Élevage"])
        nom_c = st.text_input("Nom de la culture (ex: Pomme de terre)")
        surf = st.number_input("Surface (Ha) ou Effectif", min_value=0.0, step=0.1)
        date_j = st.date_input("Date de début", datetime.now())
        
        submit = st.form_submit_button("Enregistrer sur Google Sheets")

        if submit:
            if nom_c:
                # Création de la nouvelle ligne
                new_row = pd.DataFrame([{
                    "ID": len(df) + 1,
                    "Type": type_c,
                    "Culture": nom_c,
                    "Surface": surf,
                    "Date_Debut": date_j.strftime("%Y-%m-%d"),
                    "Statut": "En cours"
                }])
                
                # Fusion avec les données existantes
                updated_df = pd.concat([df, new_row], ignore_index=True)
                
                # Mise à jour du fichier Google Sheet
                conn.update(worksheet="Campagnes", data=updated_df)
                st.success(f"✅ {nom_c} enregistré avec succès !")
                st.rerun() # Rafraîchit l'affichage
            else:
                st.error("Veuillez entrer un nom de culture.")

# --- AFFICHAGE DU TABLEAU DE BORD ---
st.subheader("📋 Registre des activités à Andal")

if df.empty:
    st.warning("Aucune donnée trouvée. Utilisez le formulaire à gauche pour commencer.")
else:
    # Affichage du tableau propre
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Petit résumé statistique
    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Campagnes", len(df))
    if "Surface" in df.columns:
        total_surf = pd.to_numeric(df["Surface"]).sum()
        c2.metric("Surface totale (Ha)", f"{total_surf:.2f}")
    c3.metric("Localisation", "Andal")

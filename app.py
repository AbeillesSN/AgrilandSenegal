import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Agriland Business", layout="wide", page_icon="💰")

# --- CONNEXION CLOUD ---
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    df = conn.read(worksheet="Campagnes")
except Exception:
    df = pd.DataFrame(columns=["ID", "Type", "Culture", "Surface", "Date_Debut", "Statut", "Depenses", "Recettes", "Resultat"])

st.title("💰 Agriland Sénégal : Suivi des Profits")

# --- FORMULAIRE DE GESTION ---
with st.sidebar:
    st.header("📈 Nouvelle Entrée")
    with st.form("compta_form"):
        type_c = st.selectbox("Catégorie", ["Maraîchage", "Arboriculture", "Élevage"])
        nom_c = st.text_input("Nom de l'activité")
        surf = st.number_input("Grandeur (Ha/Têtes)", min_value=0.0)
        depenses = st.number_input("Total Dépenses (FCFA)", min_value=0)
        recettes = st.number_input("Ventes prévues/réelles (FCFA)", min_value=0)
        
        submit = st.form_submit_button("Enregistrer le bilan")

        if submit and nom_c:
            profit = recettes - depenses
            new_row = pd.DataFrame([{
                "ID": len(df) + 1,
                "Type": type_c,
                "Culture": nom_c,
                "Surface": surf,
                "Date_Debut": datetime.now().strftime("%Y-%m-%d"),
                "Statut": "En cours",
                "Depenses": depenses,
                "Recettes": recettes,
                "Resultat": profit
            }])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(worksheet="Campagnes", data=updated_df)
            st.success(f"Bilan de {nom_c} synchronisé !")
            st.rerun()

# --- TABLEAU DE BORD FINANCIER ---
st.subheader("📊 Performance Financière à Andal")

if not df.empty:
    # Calculs des totaux
    total_dep = df["Depenses"].sum()
    total_rec = df["Recettes"].sum()
    total_prof = df["Resultat"].sum()

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Investi (FCFA)", f"{total_dep:,.0f}")
    m2.metric("Chiffre d'Affaires (FCFA)", f"{total_rec:,.0f}")
    m3.metric("Bénéfice Net (FCFA)", f"{total_prof:,.0f}", delta=f"{total_prof}")

    st.divider()
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("Enregistrez votre première campagne pour voir les statistiques.")

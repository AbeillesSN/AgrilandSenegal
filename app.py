import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Agriland Business", layout="wide", page_icon="💰")

# --- CONNEXION CLOUD ---
conn = st.connection("gsheets", type=GSheetsConnection)

# Lecture des données (Onglet "Campagnes")
try:
    df = conn.read(worksheet="Campagnes")
except:
    # Création d'une structure vide si le fichier est neuf
    df = pd.DataFrame(columns=["ID", "Type", "Culture", "Surface", "Date_Debut", "Statut", "Depenses", "Recettes", "Resultat"])

st.title("💰 Agriland Sénégal : Pilotage Financier")
st.write(f"📍 Site : Andal | État : Connecté au Cloud")

# --- INDICATEURS FINANCIERS (METRICS) ---
if not df.empty:
    # Conversion en nombres pour éviter les erreurs
    df["Depenses"] = pd.to_numeric(df["Depenses"]).fillna(0)
    df["Recettes"] = pd.to_numeric(df["Recettes"]).fillna(0)
    df["Resultat"] = pd.to_numeric(df["Resultat"]).fillna(0)
    
    col1, col2, col3 = st.columns(3)
    total_dep = df["Depenses"].sum()
    total_rec = df["Recettes"].sum()
    total_ben = df["Resultat"].sum()

    col1.metric("Total Investi", f"{total_dep:,.0f} FCFA")
    col2.metric("Ventes Totales", f"{total_rec:,.0f} FCFA")
    col3.metric("Bénéfice Net", f"{total_ben:,.0f} FCFA", delta=f"{total_ben:,.0f}")

st.divider()

# --- FORMULAIRE DE SAISIE ---
with st.sidebar:
    st.header("📈 Nouveau Bilan")
    with st.form("finance_form"):
        cat = st.selectbox("Type", ["Maraîchage", "Arboriculture", "Élevage"])
        nom = st.text_input("Culture/Espèce")
        taille = st.number_input("Surface (Ha) / Têtes", min_value=0.0)
        cout = st.number_input("Dépenses (Semences, Engrais, Main d'oeuvre)", min_value=0)
        ventes = st.number_input("Ventes (Réelles ou Estimées)", min_value=0)
        
        submit = st.form_submit_button("Enregistrer le bilan")

        if submit and nom:
            profit = ventes - cout
            new_entry = pd.DataFrame([{
                "ID": len(df) + 1,
                "Type": cat,
                "Culture": nom,
                "Surface": taille,
                "Date_Debut": datetime.now().strftime("%Y-%m-%d"),
                "Statut": "Récolté" if ventes > 0 else "En cours",
                "Depenses": cout,
                "Recettes": ventes,
                "Resultat": profit
            }])
            
            # Mise à jour du Cloud
            updated_df = pd.concat([df, new_entry], ignore_index=True)
            conn.update(worksheet="Campagnes", data=updated_df)
            st.success(f"Données pour {nom} synchronisées !")
            st.rerun()

# --- VUES DÉTAILLÉES ---
tab_complet, tab_maraichage, tab_elevage = st.tabs(["📊 Global", "🥔 Cultures", "🐓 Élevage"])

with tab_complet:
    st.dataframe(df, use_container_width=True, hide_index=True)

with tab_maraichage:
    df_m = df[df["Type"].isin(["Maraîchage", "Arboriculture"])]
    st.table(df_m[["Culture", "Surface", "Depenses", "Recettes", "Resultat"]])

with tab_elevage:
    df_e = df[df["Type"] == "Élevage"]
    st.table(df_e[["Culture", "Surface", "Depenses", "Recettes", "Resultat"]])

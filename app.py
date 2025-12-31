import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Agriland - Gestion", layout="wide", page_icon="🥔")

# --- INITIALISATION DE LA MÉMOIRE ---
if 'depenses' not in st.session_state:
    st.session_state.depenses = []

st.title("🥔 Agriland Sénégal - Spécial Pomme de Terre")
st.info("📍 Darou Khoudoss, Andal | Campagne : 5 Hectares")

# --- BARRE LATÉRALE : PARAMÈTRES & SAISIE ---
with st.sidebar:
    st.header("⚙️ Paramètres")
    date_semis = st.date_input("Date du semis", datetime(2025, 12, 19))
    prix_sac = st.number_input("Prix du sac (25kg) prévu (FCFA)", min_value=0, value=6000)
    
    st.divider()
    st.header("💸 Noter une dépense")
    motif = st.text_input("Motif (ex: Semences, Urée, Main d'oeuvre)")
    montant = st.number_input("Montant (FCFA)", min_value=0)
    if st.button("Enregistrer la dépense"):
        st.session_state.depenses.append({"Motif": motif, "Montant": montant, "Date": datetime.now().strftime("%d/%m/%Y")})
        st.success("Dépense ajoutée !")

# --- CALCULS ---
jours_passes = (datetime.now().date() - date_semis).days
recolte_totale_kg = 5 * 25 * 1000 # 5ha * 25 tonnes
nb_sacs = recolte_totale_kg / 25
chiffre_affaire = nb_sacs * prix_sac
total_depenses_reelles = sum(item['Montant'] for item in st.session_state.depenses)
benefice_reel = chiffre_affaire - total_depenses_reelles

# --- DASHBOARD ---
col1, col2, col3 = st.columns(3)
col1.metric("Âge de la culture", f"{jours_passes} jours")
col2.metric("Récolte estimée", f"{recolte_totale_kg:,} kg".replace(',', ' '))
col3.metric("Total Dépenses", f"{total_depenses_reelles:,} FCFA".replace(',', ' '))

st.divider()

# --- RENTABILITÉ RÉELLE ---
st.subheader("💰 Suivi Financier Précis")
c1, c2 = st.columns(2)
with c1:
    st.write(f"**Chiffre d'Affaire prévu :** {chiffre_affaire:,.0f} FCFA".replace(',', ' '))
    st.metric("Bénéfice Net Actuel", f"{benefice_reel:,.0f} FCFA".replace(',', ' '))
with c2:
    if st.session_state.depenses:
        st.write("**Détails des derniers frais :**")
        st.table(pd.DataFrame(st.session_state.depenses).tail(5))

# --- CALENDRIER NIAYES ---
st.subheader("📅 État de croissance")
st.progress(min(max(jours_passes / 120, 0.0), 1.0))

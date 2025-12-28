import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Agriland - Pomme de Terre", layout="wide", page_icon="🥔")

st.title("🥔 Agriland Sénégal - Spécial Pomme de Terre")
st.info("📍 Darou Khoudoss, Andal | Campagne : 5 Hectares")

# --- PARAMÈTRES TECHNIQUES ---
SURFACE = 5
COUT_HA_ESTIME = 450000  # FCFA (Semences, engrais, main d'oeuvre)
RENDEMENT_MOYEN = 25     # Tonnes par Ha (moyenne Niayes)

# --- SAISIE DES DONNÉES ---
with st.sidebar:
    st.header("⚙️ Paramètres Campagne")
    date_semis = st.date_input("Date du semis", datetime(2023, 11, 15))
    prix_sac = st.number_input("Prix du sac (25kg) prévu (FCFA)", min_value=0, value=10000)

# --- CALCULS AUTOMATIQUES ---
jours_passes = (datetime.now().date() - date_semis).days
date_recolte = date_semis + timedelta(days=120)
recolte_totale_kg = SURFACE * RENDEMENT_MOYEN * 1000
nb_sacs = recolte_totale_kg / 25
chiffre_affaire = nb_sacs * prix_sac
benefice = chiffre_affaire - (SURFACE * COUT_HA_ESTIME)

# --- AFFICHAGE DASHBOARD ---
col1, col2, col3 = st.columns(3)
col1.metric("Âge de la culture", f"{jours_passes} jours")
col2.metric("Récolte estimée", f"{recolte_totale_kg:,} kg".replace(',', ' '))
col3.metric("Date de récolte", date_recolte.strftime("%d/%b/%Y"))

st.divider()

# --- ANALYSE FINANCIÈRE PRÉVISIONNELLE ---
st.subheader("💰 Estimation de la Rentabilité")
c1, c2 = st.columns(2)
with c1:
    st.write(f"**Nombre de sacs (25kg) :** {nb_sacs:,.0f}".replace(',', ' '))
    st.write(f"**Chiffre d'Affaire prévu :** {chiffre_affaire:,.0f} FCFA".replace(',', ' '))
with c2:
    color = "normal" if benefice > 0 else "inverse"
    st.metric("Bénéfice Net Estimé", f"{benefice:,.0f} FCFA".replace(',', ' '), delta_color=color)

# --- CALENDRIER NIAYES ---
st.subheader("📅 État de croissance")
progress = min(max(jours_passes / 120, 0.0), 1.0)
st.progress(progress)

if jours_passes < 30:
    st.success("🌱 Phase de levée : Surveillez l'irrigation régulière.")
elif 30 <= jours_passes < 70:
    st.warning("🌿 Phase de tubérisation : Moment crucial pour l'apport en Potassium (K).")
elif 70 <= jours_passes < 100:
    st.info("🥔 Grossissement des tubercules : Maintenez une humidité constante.")
else:
    st.error("🚜 Maturité : Préparez la récolte et le stockage à l'ombre.")

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Agriland - Pomme de Terre", layout="wide")

st.title("🥔 Gestion Campagne Pomme de Terre")
st.write("📍 Site : Andal, Darou Khoudoss")

# Paramètres de la culture
SURFACE = 5 # hectares
CYCLE = 120 # jours

# Barre latérale pour les entrées
st.sidebar.header("Nouvelle Opération")
date_semis = st.sidebar.date_input("Date du semis", datetime(2023, 11, 15)) # Date par défaut
type_op = st.sidebar.selectbox("Action", ["Irrigation", "Fertilisation (NPK/Urée)", "Traitement Phytosanitaire", "Buttage", "Récolte"])
quantite = st.sidebar.number_input("Quantité utilisée (kg ou L)", min_value=0.0)

if st.sidebar.button("Enregistrer l'opération"):
    st.sidebar.success(f"Opération '{type_op}' enregistrée !")

# --- TABLEAU DE BORD DES 5 HA ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Surface", f"{SURFACE} Ha")
with col2:
    # Calcul des jours restants
    jours_passes = (datetime.now().date() - date_semis).days
    st.metric("Âge de la culture", f"{jours_passes} jours")
with col3:
    date_recolte = date_semis + timedelta(days=CYCLE)
    st.metric("Récolte prévue", date_recolte.strftime("%d/%m/%Y"))

# --- ALERTES ET CONSEILS (ZONE NIAYES) ---
st.subheader("💡 Recommandations du jour")
if 30 <= jours_passes <= 45:
    st.warning("Période critique : C'est le moment idéal pour le deuxième apport d'engrais et le buttage.")
elif jours_passes > 110:
    st.error("Attention : Réduisez l'irrigation pour préparer la maturité des tubercules.")
else:
    st.info("Continuez le suivi régulier de l'irrigation (fréquence élevée dans les Niayes).")

# Simulation de suivi financier
st.subheader("💰 Estimation des charges")
st.write(f"Coût estimé des semences et engrais pour 5 Ha : **{SURFACE * 450000} FCFA** (base indicative)")

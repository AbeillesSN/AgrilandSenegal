import streamlit as st
import pandas as pd

st.set_page_config(page_title="Agriland Sénégal", layout="wide")

st.title("🚜 Agriland Sénégal - Gestion de la Ferme")
st.write("Bienvenue dans votre outil de pilotage à Darou Khoudoss.")

# Menu simple pour commencer
option = st.sidebar.selectbox("Choisir un module", ["Cultures", "Élevage", "Stocks"])

if option == "Cultures":
    st.header("Suivi des 5ha de Pomme de terre")
    st.info("Ici vous pourrez suivre l'arrosage et les traitements.")

elif option == "Élevage":
    st.header("Suivi des Poulets et Bovins")
    st.success("Module pour la ponte et la santé animale.")

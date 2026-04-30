import streamlit as st
import pandas as pd
import os
from datetime import datetime

FICHIER_DONNEES = "donnees_collecte.csv"

st.set_page_config(page_title="BD collecte", page_icon=" ")

st.title("BD collecte - Agence Hospitalière")

with st.form("form_collecte", clear_on_submit=True):
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    ville = st.text_input("Ville")
    email = st.text_input("Email")
    
    # --- AJOUT DES HEURES ---
    col1, col2 = st.columns(2)
    with col1:
        heure_arrivee = st.time_input("Heure d'arrivée", value=None)
    with col2:
        heure_fin = st.time_input("Heure de fin", value=None)
    
    submit = st.form_submit_button("Enregistrer les données")

if submit:
    # Vérification que tous les champs sont remplis (y compris les heures)
    if nom and prenom and ville and email and heure_arrivee and heure_fin:
        nouvelle_donnee = {
            "Date": datetime.now().strftime("%d/%m/%Y"),
            "Nom": nom,
            "Prenom": prenom,
            "Ville": ville,
            "Email": email,
            "Arrivée": heure_arrivee.strftime("%H:%M"), # Formatage de l'heure
            "Fin": heure_fin.strftime("%H:%M")
        }
       
        try:
            if not os.path.isfile(FICHIER_DONNEES):
                df_nouveau.to_csv(FICHIER_DONNEES, index=False, encoding='utf-8')
            else:
                df_nouveau.to_csv(FICHIER_DONNEES, mode='a', header=False, index=False, encoding='utf-8')
            st.success(f" Enregistré pour {prenom} {nom} ({heure_arrivee} - {heure_fin})")
        except Exception as e:
            st.error(f"Erreur : {e}")
    else:
        st.error(" Veuillez remplir tous les champs, y compris les heures.")

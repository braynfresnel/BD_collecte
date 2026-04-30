   import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Nom du fichier
FICHIER_DONNEES = "donnees_collecte.csv"

st.set_page_config(page_title="BD collecte", page_icon=" ")

st.title("BD collecte - Agence Hospitalière")
st.subheader("Formulaire de collecte quotidienne des données")

# --- FORMULAIRE ---
with st.form("form_collecte", clear_on_submit=True):
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    ville = st.text_input("Ville")
    email = st.text_input("Email")
    
    submit = st.form_submit_button("Enregistrer les données")

# --- TRAITEMENT DES DONNÉES ---
if submit:
    if nom and prenom and ville and email:
        nouvelle_donnee = {
            "Date": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Nom": nom,
            "Prenom": prenom,
            "Ville": ville,
            "Email": email
        }
        
        df_nouveau = pd.DataFrame([nouvelle_donnee])
        
        # Sauvegarde sécurisée
        try:
            if not os.path.isfile(FICHIER_DONNEES):
                df_nouveau.to_csv(FICHIER_DONNEES, index=False, encoding='utf-8')
            else:
                df_nouveau.to_csv(FICHIER_DONNEES, mode='a', header=False, index=False, encoding='utf-8')
            
            st.success(f" Données enregistrées pour {prenom} {nom} !")
        except Exception as e:
            st.error(f"Erreur lors de l'enregistrement : {e}")
    else:
        st.error(" Veuillez remplir tous les champs avant de valider.")

# --- ADMINISTRATION ---
st.sidebar.header("Administration")
if st.sidebar.checkbox("Afficher les données collectées"):
    if os.path.isfile(FICHIER_DONNEES):
        # On utilise une clé différente pour éviter les conflits de lecture/écriture
        df_affiche = pd.read_csv(FICHIER_DONNEES)
        st.write(df_affiche)
        
        # Préparation du téléchargement
        csv_data = df_affiche.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button(
            label=" Télécharger le fichier CSV",
            data=csv_data,
            file_name="collecte_hospitaliere.csv",
            mime="text/csv"
        )
    else:
        st.sidebar.info("Aucune donnée enregistrée pour le moment.")
     

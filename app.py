import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Nom du fichier de stockage
FICHIER_DONNEES = "donnees_collecte.csv"

# Configuration de la page
st.set_page_config(page_title="BD collecte", page_icon="🏥")

# --- INITIALISATION DE LA MÉMOIRE (SESSION STATE) ---
# On crée des variables vides si elles n'existent pas encore
if 'etape' not in st.session_state:
    st.session_state.etape = 1
if 'infos_perso' not in st.session_state:
    st.session_state.infos_perso = {}

st.title("🏥 BD collecte - Agence Hospitalière")

# --- ÉTAPE 1 : INFORMATIONS PERSONNELLES ---
if st.session_state.etape == 1:
    st.subheader("Étape 1 : Informations personnelles")
    
    with st.form("form_etape1"):
        nom = st.text_input("Nom", value=st.session_state.infos_perso.get('nom', ''))
        prenom = st.text_input("Prénom", value=st.session_state.infos_perso.get('prenom', ''))
        ville = st.text_input("Ville", value=st.session_state.infos_perso.get('ville', ''))
        email = st.text_input("Email", value=st.session_state.infos_perso.get('email', ''))
        
        submit1 = st.form_submit_button("Suivant ➡️")
        
        if submit1:
            if nom and prenom and ville and email:
                # Sauvegarde temporaire des infos
                st.session_state.infos_perso = {
                    "nom": nom,
                    "prenom": prenom,
                    "ville": ville,
                    "email": email
                }
                # Passage à l'étape 2
                st.session_state.etape = 2
                st.rerun() # Relance l'application pour afficher l'étape 2
            else:
                st.error("Veuillez remplir tous les champs.")

# --- ÉTAPE 2 : HEURES DE SERVICE ---
elif st.session_state.etape == 2:
    st.subheader(f"Étape 2 : Horaires pour {st.session_state.infos_perso['prenom']}")
    
    with st.form("form_etape2"):
        # Sélection de l'heure
        heure_arrivee = st.time_input("Heure d'arrivée")
        heure_depart = st.time_input("Heure de fin")
        
        col1, col2 = st.columns(2)
        with col1:
            retour = st.form_submit_button("⬅️ Retour")
        with col2:
            valider = st.form_submit_button("Enregistrer définitivement ✅")

        if retour:
            st.session_state.etape = 1
            st.rerun()

        if valider:
            # Préparation de la ligne complète
            nouvelle_donnee = {
                "Date": datetime.now().strftime("%d/%m/%Y"),
                "Nom": st.session_state.infos_perso['nom'],
                "Prenom": st.session_state.infos_perso['prenom'],
                "Ville": st.session_state.infos_perso['ville'],
                "Email": st.session_state.infos_perso['email'],
                "Heure_Arrivee": heure_arrivee.strftime("%H:%M"),
                "Heure_Fin": heure_depart.strftime("%H:%M")
            }
            
            # Sauvegarde dans le CSV
            df_nouveau = pd.DataFrame([nouvelle_donnee])
            if not os.path.isfile(FICHIER_DONNEES):
                df_nouveau.to_csv(FICHIER_DONNEES, index=False, encoding='utf-8')
            else:
                df_nouveau.to_csv(FICHIER_DONNEES, mode='a', header=False, index=False, encoding='utf-8')
            
            # Confirmation et réinitialisation
            st.success("Données enregistrées avec succès !")
            st.balloons() # Petite animation de fête
            
            # On remet l'application à zéro pour le suivant
            st.session_state.etape = 1
            st.session_state.infos_perso = {}
            # On pourrait ajouter un bouton pour recommencer ou utiliser un timer
            if st.button("Faire une nouvelle saisie"):
                st.rerun()

# --- VISUALISATION (Dans la barre latérale) ---
st.sidebar.header("Administration")
if st.sidebar.checkbox("Voir la liste des présences"):
    if os.path.isfile(FICHIER_DONNEES):
        df_affiche = pd.read_csv(FICHIER_DONNEES)
        st.sidebar.write(df_affiche)
    else:
        st.sidebar.info("Aucune donnée enregistrée.")
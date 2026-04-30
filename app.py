import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Nom du fichier de stockage
FICHIER_DONNEES = "donnees_collecte.csv"

# Configuration de la page (Mode large pour mieux voir le tableau)
st.set_page_config(page_title="BD collecte", page_icon=" ", layout="wide")

st.title("BD collecte - Agence Hospitalière")
st.subheader("Formulaire de collecte quotidienne")

# --- ZONE DE SAISIE (PRINCIPALE) ---
with st.form("form_collecte", clear_on_submit=True):
    st.write("###  Remplir les informations")
    
    col_a, col_b = st.columns(2)
    with col_a:
        nom = st.text_input("Nom")
        ville = st.text_input("Ville")
    with col_b:
        prenom = st.text_input("Prénom")
        email = st.text_input("Email")
    
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        # Utilise l'heure actuelle comme valeur par défaut
        heure_arrivee = st.time_input("Heure d'arrivée", value=datetime.now().time())
    with col2:
        heure_fin = st.time_input("Heure de fin", value=datetime.now().time())
    
    submit = st.form_submit_button("Enregistrer les données")

# --- LOGIQUE D'ENREGISTREMENT ---
if submit:
    # On vérifie que les champs de texte ne sont pas vides
    if nom and prenom and ville and email:
        nouvelle_donnee = {
            "Date": datetime.now().strftime("%d/%m/%Y"),
            "Nom": nom.upper(), # Nom en majuscules pour la propreté
            "Prenom": prenom.capitalize(),
            "Ville": ville,
            "Email": email,
            "Arrivee": heure_arrivee.strftime("%H:%M"),
            "Fin": heure_fin.strftime("%H:%M")
        }
        
        df_nouveau = pd.DataFrame([nouvelle_donnee])
        
        try:
            # Si le fichier n'existe pas, on le crée avec l'en-tête
            if not os.path.isfile(FICHIER_DONNEES):
                df_nouveau.to_csv(FICHIER_DONNEES, index=False, encoding='utf-8')
            else:
                # Sinon on ajoute la ligne à la fin sans répéter l'en-tête
                df_nouveau.to_csv(FICHIER_DONNEES, mode='a', header=False, index=False, encoding='utf-8')
            
            # Message de succès (S'affichera bien car il n'y a plus de st.rerun)
            st.success(f" Les informations de {prenom} {nom} ont été enregistrées avec succès !")
            st.balloons() 
            
        except Exception as e:
            st.error(f"❌ Erreur technique lors de l'enregistrement : {e}")
    else:
        st.error(" Attention : Veuillez remplir tous les champs du formulaire.")

# --- ZONE D'ADMINISTRATION (SIDEBAR) ---
st.sidebar.header(" Administration")

# Option pour afficher les données
afficher = st.sidebar.checkbox("Afficher la base de données")

if afficher:
    st.sidebar.divider()
    if os.path.isfile(FICHIER_DONNEES):
        # Lecture du fichier
        df_affiche = pd.read_csv(FICHIER_DONNEES)
        
        # Affichage du nombre d'inscrits
        st.sidebar.metric("Total inscrits", len(df_affiche))
        
        # Affichage du tableau sur la page principale
        st.write("---")
        st.write("###  Liste des personnes enregistrées")
        st.dataframe(df_affiche, use_container_width=True)
        
        # Préparation du bouton de téléchargement
        csv_data = df_affiche.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button(
            label="Télécharger le fichier CSV",
            data=csv_data,
            file_name=f"collecte_{datetime.now().strftime('%d_%m_%Y')}.csv",
            mime="text/csv"
        )
    else:
        st.sidebar.info(" Aucune donnée n'a encore été enregistrée.")

   
     

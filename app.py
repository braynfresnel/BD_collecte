import streamlit as st
import pandas as pd
import os
from datetime import datetime

FICHIER_DONNEES = "donnees_collecte.csv"

st.set_page_config(page_title="BD collecte", page_icon="🏥", layout="wide")

st.title("🏥 BD collecte - Agence Hospitalière")

# --- FORMULAIRE ---
with st.form("form_collecte", clear_on_submit=True):
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    ville = st.text_input("Ville")
    email = st.text_input("Email")
    
    col1, col2 = st.columns(2)
    with col1:
        # On met l'heure actuelle par défaut au lieu de None
        heure_arrivee = st.time_input("Heure d'arrivée", value=datetime.now().time())
    with col2:
        heure_fin = st.time_input("Heure de fin", value=datetime.now().time())
    
    submit = st.form_submit_button("Enregistrer les données")

if submit:
    # On vérifie juste les textes, les heures ont forcément une valeur par défaut
    if nom and prenom and ville and email:
        nouvelle_donnee = {
            "Date": datetime.now().strftime("%d/%m/%Y"),
            "Nom": nom,
            "Prenom": prenom,
            "Ville": ville,
            "Email": email,
            "Arrivee": heure_arrivee.strftime("%H:%M"),
            "Fin": heure_fin.strftime("%H:%M")
        }
        df_nouveau = pd.DataFrame([nouvelle_donnee])
        
        try:
            if not os.path.isfile(FICHIER_DONNEES):
                df_nouveau.to_csv(FICHIER_DONNEES, index=False, encoding='utf-8')
            else:
                df_nouveau.to_csv(FICHIER_DONNEES, mode='a', header=False, index=False, encoding='utf-8')
            st.balloons()
            st.success("✅ Enregistré avec succès !")
            st.rerun() # Force la mise à jour pour voir le résultat
        except Exception as e:
            st.error(f"Erreur d'écriture : {e}")
    else:
        st.error("⚠️ Veuillez remplir tous les champs de texte.")

# --- SIDEBAR ---
st.sidebar.header("Administration")
if st.sidebar.checkbox("Afficher les données"):
    if os.path.isfile(FICHIER_DONNEES):
        df = pd.read_csv(FICHIER_DONNEES)
        st.sidebar.metric("Total", len(df))
        st.write("### Liste des inscrits")
        st.dataframe(df, use_container_width=True)
    else:
        st.sidebar.write("Aucune donnée.")

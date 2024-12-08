import streamlit as st
import pandas as pd
from pathlib import Path
from utils import clean
from firebase_utils import tirage, get_tirage_idee, add_idee

APP_NAME = 'NOEL'
# Load the data

st.title("🎅🎄 Secret Santa 2024")
st.sidebar.title("La bible du Secret Santa Lavaud-Millon-Adnet 🎅🎄")

with st.sidebar.info("**⭐️Les règles du jeu ⭐️**"):
    st.markdown("""
    - Tirer au sort le nom de la personne à qui tu vas offrir un cadeau 🧚‍♀️
    - Donne des idées de cadeau pour la personne qui te tirera au sort! 🎁
    """)
   
with st.sidebar.success("ℹ️ **PSSSSS: Comment faire les cadeaux**"):
    st.markdown("""On respecte un budget de 50€ pour les cadeaux du Secret Santa!! 💶""")

st.sidebar.caption("Réalisé par Chloé Adnet")


## Get Data
data_path = Path.cwd() / "secret_santa" / "data" 
family_path = data_path / "family_members.csv"
family = pd.read_csv(family_path)

firestore_certificate_path = data_path / "firestore_certificate.json"
firebase_url = "https://secretsanta-8da89-default-rtdb.firebaseio.com"

first_name = clean(st.text_input("Entre ton prénom:"))
last_name = clean(st.text_input("Entre ton nom de famille:"))
identifiant = None

if st.button("1️⃣ Click pour enregistrer ton nom et prénom "):
    identifiant = first_name + last_name
    st.write("Merci, tu peux continuer! ⭐️")


if st.button("2️⃣ Je tire au sort la personne à laquelle offrir un cadeau"):
    identifiant = first_name + last_name
    if identifiant is not None:
        identifiant_tire = tirage(identifiant)
        personne = family[family['identifiant'] == identifiant_tire]
        prenom = personne['prenom'].values[0].title()
        nom = personne['nom'].values[0].title()
        st.write(f"Personne tirée :  {prenom} {nom}")
    else: 
        st.write("❌ Il faut que tu enregistres ton nom et ton prénom")

st.text("Tu peux ajouter plusieurs idées, à plusieurs moment différent!\n A chaque fois que tu donneras une nouvelle idée, elle sera ajoutée à la liste des précédents!")
idee = st.text_input("🎁 Mes idées de cadeau")
if st.button("3️⃣ J'enregistre mes idées de cadeau 🎄"):
   identifiant = first_name + last_name
   if identifiant is not None:
        add_idee(identifiant, idee)
        st.write("Super, ton idée a bien été notée! 🚀")
   else: 
        st.write("❌ Il faut que tu enregistres ton nom et ton prénom")


if st.button("4️⃣ Je découvre les idées cadeau de la personne que j'ai tiré!"):
    identifiant = first_name + last_name
    if identifiant is not None:
        idees = get_tirage_idee(identifiant)
        st.write(idees)
    else: 
            st.write("❌ Il faut que tu enregistres ton nom et ton prénom")
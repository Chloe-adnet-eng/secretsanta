import streamlit as st
import pandas as pd
from pathlib import Path
from utils import clean
from firebase_utils import tirage, get_tirage_idee, add_idee
import requests

APP_NAME = 'NOEL'
# Load the data

st.title("🎅🎄 Secret Santa 2024")
st.sidebar.title("La bible du Secret Santa Lavaud-Millon-Adnet 🎅🎄")


gif_url = 'https://media.giphy.com/media/3o6wrglt7FjpTnmyEE/giphy.gif'
response = requests.get(gif_url)
st.image(response.content, use_container_width=True)

with st.sidebar.info("**⭐️Les règles du jeu ⭐️**"):
    st.markdown("""
                
    ## S'enregsitrer 📓
    - Entre ton prénom et ton nom de famille
    - Clique pour enregistrer ton nom et prénom
    - Tu ne pourras pas continuer sans t'enregistrer 🤧 et donc tu n'auras pas de cadeaux 😭
                
    ## Tirer au sort 😱
    - Après t'être enregistré, clique pour tirer au sort la personne à qui tu vas offrir un cadeau! 
    
    
    ##  Ajouter de nouvelles idées de cadeaux 🎁
    - Tu peux revenir autant de fois que tu le souhaites 🙂
    - Il faut toujours remplir ton *prénom* et ton *nom* et *enregistrer* 
    - Puis tu pourras ajouter des idées de cadeaux autant que tu le souhaite!
                
    ## 🐛 Pour tout bug
    - Contacte Chloé Adnet 📧
    """)
   
with st.sidebar.success("ℹ️ **PSSSSS: Comment faire les cadeaux**"):
    st.markdown("""On respecte un budget de 50€ pour les cadeaux du Secret Santa!! 💶""")
    gif_url = 'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNGhjaXFlZDhhMzl5MW0yNW9tNnVmczZ1NjB1YmFodW9janNwbDg5YiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/XcjH630Kf8Yr3FOy6E/giphy.gif'
    response = requests.get(gif_url)
    st.image(response.content, use_container_width=True)
    
st.sidebar.caption("Réalisé par Chloé Adnet")


## Get Data
data_path = Path.cwd() / "secret_santa" / "data" 
family_path = data_path / "family_members.csv"
family = pd.read_csv(family_path)

first_name = clean(st.text_input("Entre ton prénom:"))
last_name = clean(st.text_input("Entre ton nom de famille:"))
identifiant = None

if st.button("1️⃣ Click pour enregistrer ton nom et prénom "):
    identifiant = first_name + last_name
    st.write("Merci, tu peux continuer! ⭐️")


if st.button("2️⃣ Je tire au sort la personne à laquelle offrir un cadeau"):
    identifiant = first_name + last_name
    if first_name == "" or last_name == "" or first_name is None or last_name is None:
        st.write("❌ Il faut que tu enregistres ton nom et ton prénom")
    elif identifiant is not None:
        identifiant_tire = tirage(identifiant)
        personne = family[family['identifiant'] == identifiant_tire]
        prenom = personne['prenom'].values[0].title()
        nom = personne['nom'].values[0].title()
        st.markdown(f'''## La personne que tu as tiré est : :rainbow[{prenom} {nom}]
        ''')

if st.button("3️⃣ Je découvre les idées cadeau de la personne que j'ai tiré!"):
    identifiant = first_name + last_name
    if first_name == "" or last_name == "" or first_name is None or last_name is None:
        st.write("❌ Il faut que tu enregistres ton nom et ton prénom")
    elif identifiant is not None:
        idees = get_tirage_idee(identifiant)
        st.write(idees)
    else: 
        st.write("❌ Il faut que tu enregistres ton nom et ton prénom")

st.markdown(f'''## Mes idées de  :rainbow[cadeau!]
        ''')
st.text("A chaque fois que tu donneras une nouvelle idée, elle sera ajoutée à la liste des précédents!")
st.text("N'oublie pas d'enregistrer ton prénom et ton nom avant de donner des idées de cadeau! 🎅🎄")
idee = st.text_input("🎁 Mes idées de cadeau")
if st.button("♾️J'enregistre mes idées de cadeau 🎄"):
   identifiant = first_name + last_name
   if first_name == "" or last_name == "" or first_name is None or last_name is None:
        st.write("❌ Il faut que tu enregistres ton nom et ton prénom")
   elif identifiant is not None:
        add_idee(identifiant, idee)
        st.write("Super, ton idée a bien été notée! 🚀")







gif_url = 'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExcXd6cmdnd3pseTc5cnJnem44dHA0cTFmNDh1ZWNoNTh1Yml3cnljciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/RGMjyQmBVhNpcfuMnB/giphy.gif'
response = requests.get(gif_url)
st.image(response.content, use_container_width=True)
import streamlit as st
import pandas as pd
from pathlib import Path
from utils import clean
from firebase_utils import tirage, get_tirage_idee, add_idee, get_my_tirage_idee
import requests

APP_NAME = 'NOEL'
# Load the data

st.title("🎅🎄 Secret Santa 2024")
st.sidebar.title("La bible du Secret Santa Lavaud-Millon-Adnet 🎅🎄")

# Réduire la taille des GIFs
gif_url = 'https://media.giphy.com/media/3o6wrglt7FjpTnmyEE/giphy.gif'
response = requests.get(gif_url)
st.image(response.content, use_container_width=True, width=500)

with st.sidebar.info("**⭐️Les règles du jeu ⭐️**"):
    st.markdown("""
    ## S'enregsitrer 📓
    - Sélectionne ton prénom et ton nom dans la liste
    - Tu ne pourras pas continuer sans te sélectionner 🤧 et donc tu n'auras pas de cadeaux 😭
                
    ## Tirer au sort 😱
    - Après t'être sélectionné, clique pour tirer au sort la personne à qui tu vas offrir un cadeau! 
    
    ## Ajouter de nouvelles idées de cadeaux 🎁
    - Tu peux revenir autant de fois que tu le souhaites 🙂
    - Il faut toujours te sélectionner avant d'ajouter une idée
    - Puis tu pourras ajouter des idées de cadeaux autant que tu le souhaites!
                
    ## 🐛 Pour tout bug
    - Contacte Chloé Adnet 📧
    """)
   
with st.sidebar.success("ℹ️ **PSSSSS: Comment faire les cadeaux**"):
    st.markdown("""On respecte un budget de 50€ pour les cadeaux du Secret Santa!! 💶""")
    gif_url = 'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNGhjaXFlZDhhMzl5MW0yNW9tNnVmczZ1NjB1YmFodW9janNwbDg5YiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/XcjH630Kf8Yr3FOy6E/giphy.gif'
    response = requests.get(gif_url)
    st.image(response.content, use_container_width=True, width=500)

st.sidebar.caption("Réalisé par Chloé Adnet")

## Get Data
data_path = Path.cwd() / "secret_santa" / "data" 
family_path = data_path / "family_members.csv"
family = pd.read_csv(family_path)

# Get the list of full names to display in the selectbox
family_names = (family['prenom'] + ' ' + family['nom']).str.title()

# Authentification avec sélection obligatoire
selected_name = st.selectbox("Sélectionne ton prénom et nom", family_names)

if selected_name:
    first_name, last_name = selected_name.split(' ')
    first_name = clean(first_name)
    last_name = clean(last_name)
    
    # Confirmation d'enregistrement du nom
    if st.button("✅ Je me suis sélectionné! 🎅"):
        st.write(f"Merci {first_name.title()}, tu peux continuer! ⭐️")

    # Tirage de la personne à qui offrir un cadeau
    if st.button("2️⃣ Je tire au sort la personne à laquelle offrir un cadeau"):
        identifiant = first_name + last_name
        identifiant_tire = tirage(identifiant)
        personne = family[family['identifiant'] == identifiant_tire]
        prenom = personne['prenom'].values[0].title()
        nom = personne['nom'].values[0].title()
        st.markdown(f'''### La personne que tu as tiré est : {prenom} {nom}''')

    # Voir les idées cadeau de la personne tirée
    if st.button("3️⃣ Je découvre les idées cadeau de la personne que j'ai tiré!"):
        identifiant = first_name + last_name
        idees = get_tirage_idee(identifiant)
        if idees:
            st.write("Voici les idées de cadeau de la personne que tu as tirée :")
            st.write(idees)
        else:
            st.write("Aucune idée de cadeau disponible pour cette personne.")

    st.markdown(f'''## Mes idées de cadeau! 🎁''')
    
    # Explication sur comment ajouter une idée de cadeau
    with st.expander("📚 Comment ajouter une idée de Cadeau!"):

        st.markdown("""
        - **Étape 1** : Sélectionne toujours ton prénom et nom avant d'ajouter une idée de cadeau.
        - **Étape 2** : Ajoute une idée de cadeau à la liste: autant de fois que tu le souhaites! 🎅
        - **Étape 3** : Après avoir ajouté une idée, tu peux la consulter à tout moment.
        """)

    # Section pour ajouter des idées de cadeau
    idee = st.text_input("🎁 Mes idées de cadeau")

    # Enregistrer les idées de cadeau
    if st.button("♾️J'enregistre mes idées de cadeau 🎄"):
        identifiant = first_name + last_name
        add_idee(identifiant, idee)
        st.write("Super, ton idée a bien été notée! 🚀")

    # Voir les idées de cadeau enregistrées
    if st.button("🎁 Voir mes idées de cadeau"):
        idees = get_my_tirage_idee(first_name + last_name)  # Récupérer les idées de cadeau
        if idees:
            st.write("Voici tes idées de cadeau sauvegardées :")
            st.write(idees)
        else:
            st.write("Aucune idée de cadeau enregistrée pour le moment.")
            
# Réduire la taille du gif final
gif_url = 'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExcXd6cmdnd3pseTc5cnJnem44dHA0cTFmNDh1ZWNoNTh1Yml3cnljciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/RGMjyQmBVhNpcfuMnB/giphy.gif'
response = requests.get(gif_url)
st.image(response.content, use_container_width=True, width=500)

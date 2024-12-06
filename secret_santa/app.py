import streamlit as st
import pandas as pd
from pathlib import Path
from utils import check_member, clean, get_random_family_member
# Load the data

data_path = Path.cwd() / "secret_santa" /"data" 
family_path = data_path / "family_members.csv"
family = pd.read_csv(family_path)


st.title("🎄 Secret Santa Lavaud, Adnet, Millon 🎄")
st.write("Hello la famille !")

first_name = clean(st.text_input("Entre ton prénom:"))
last_name = clean(st.text_input("Entre ton nom de famille:"))

is_member = check_member(first_name, last_name, family)

if st.button("Check si tu es membre de la famille"):
    if is_member:
        st.write(f"Bonjour {first_name.title()} {last_name.title()}, tu es bien membre de la famille 😁")
    else:
        st.write(f"Désolé {first_name.title()} {last_name.title()}, tu n'es pas membre de la famille 😢")

if st.button("Tire au sort le nom de la personne à qui tu vas offrir un cadeau"):
    if not is_member:
        st.write("Tu dois être membre de la famille pour participer au tirage au sort 🎅")
    else:
        prenom, nom = get_random_family_member(family, first_name, last_name)
        st.write(f"Tu vas offrir un cadeau à {prenom} {nom} 🎁")

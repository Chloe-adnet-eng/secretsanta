import streamlit as st
import pandas as pd
from pathlib import Path
from utils import check_member, clean, get_random_family_member
from PIL import Image
# Load the data

data_path = Path.cwd() / "secret_santa" /"data" 
family_path = data_path / "family_members.csv"
family = pd.read_csv(family_path)


st.title("🎄 Secret Santa Lavaud, Adnet, Millon 🎄")
st.write("Hello la famille !")

pic_path = data_path / "family_picture.jpg"
image = Image.open(pic_path)
st.image(image, caption="La famille Lavaud, Adnet, Millon fête noël 🎅", width=320)

first_name = clean(st.text_input("Entre ton prénom:"))
last_name = clean(st.text_input("Entre ton nom de famille:"))

is_member = check_member(first_name, last_name, family)

if st.button("🥁 Tire au sort le nom de la personne à qui tu vas offrir un cadeau"):
    if not is_member:
        st.write(f"Tu dois d'abord être membre de la famille pour participer au tirage au sort 🎁")
    else:
        random_member = get_random_family_member(family, first_name, last_name)
        st.write(f"Tu vas offrir un cadeau à {random_member[0].title()} {random_member[1].title()} 🎁")
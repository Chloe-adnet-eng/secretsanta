import streamlit as st
import pandas as pd
from pathlib import Path
from secret_santa.utils import check_member, clean
# Load the data

data_path = Path.cwd() / 'secret_santa' /'data' 
family_path = data_path / 'family_members.csv'
family = pd.read_csv(family_path)


st.title('🎄 Secret Santa Lavaud, Adnet, Millon 🎄')
st.write("Hello la famille !")

first_name = st.text_input('Entre ton prénom:')
last_name = st.text_input('Entre ton nom de famille:')



if st.button('Check si tu es membre de la famille'):
    first_name = clean(first_name)
    last_name = clean(last_name)
    if check_member(first_name, last_name, family):

        st.write(f"Bonjour {first_name.title()} {last_name.title()}, tu es bien membre de la famille 😁")
    else:
        st.write(f"Désolé {first_name.title()} {last_name.title()}, tu n'es pas membre de la famille 😢")

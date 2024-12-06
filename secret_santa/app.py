import streamlit as st
import pandas as pd
from pathlib import Path

# Load the data

data_path = Path.cwd() / 'secret_santa' /'data' 
family_path = data_path / 'family_members.csv'
family = pd.read_csv(family_path)


st.title('🎄 Secret Santa Lavaud, Adnet, Millon 🎄')
st.write("Hello la famille !")


st.write(family)
st.table(family)

st.dataframe(family.style.highlight_max(axis=0))
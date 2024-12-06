import pandas as pd
from unidecode import unidecode

def check_member(prenom: str, nom: str, family: pd.DataFrame):
    if prenom not in family["prenom"].values:
        return False
    noms = family[family["prenom"] == prenom]
    if nom not in noms["nom"].values:
        return False
    return True
    
def clean(text: str):
    return unidecode(text.lower())

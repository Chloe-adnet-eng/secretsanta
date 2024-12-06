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

def create_member_identifier(family: pd.DataFrame) -> pd.DataFrame:
    family["member_id"] = family["prenom"] + family["nom"]
    return family

def get_random_family_member(family: pd.DataFrame, prenom: str, nom: str):
    """_summary_
        Given a family member, return a random other family member
    """
    family_with_identifier = create_member_identifier(family)
    member_id = prenom + nom
    family_without_member = family_with_identifier[family_with_identifier["member_id"] != member_id]
    random_member = family_without_member.sample(1)
    return random_member["prenom"].values[0].title(), random_member["nom"].values[0].title()
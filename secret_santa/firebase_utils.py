from typing import Optional
import firebase_admin
from firebase_admin import credentials, db
from firebase_admin.db import Reference
import pandas as pd
import streamlit as st
from pathlib import Path
import random

data_path = Path.cwd() / "secret_santa" / "data" 

FAMILY_PATH = data_path / "family_members.csv"
FIRESTORE_CERTIFICATE_PATH = data_path / "secret_santa_cred.json"
FIREBASE_URL = "https://secretsanta-8da89-default-rtdb.firebaseio.com"

def get_app_credentials():
    if Path.exists(FIRESTORE_CERTIFICATE_PATH):  
        cred = credentials.Certificate(str(FIRESTORE_CERTIFICATE_PATH))
    else:
        cred = credentials.Certificate(st.secrets['firebase_certificate'])
    return cred

def delete_app() -> None:
    firebase_admin.delete_app(firebase_admin.get_app())

def get_app_reference() -> Optional[Reference]:
    try:    
        print(f"Trying to get app")
        firebase_admin.get_app()
        print(f"Firebase app is already initialized.")
    except ValueError:
        print(f"Initializing Firebase app")
        cred = get_app_credentials()
        firebase_admin.initialize_app(
            cred,
            {
                'databaseURL': FIREBASE_URL
            },
        )
        print(f"Firebase app has been initialized.")
    try :
        return db.reference()
    except Exception as e:
        print(f"The app isn't initialized yet. {e}")
        return None

def get_all_data() -> dict:
    
    app_reference: Reference = get_app_reference()
    
    app_data = app_reference.get()
    
    delete_app()

    return app_data

def get_data(key:str) -> dict:

    app_reference: Reference = get_app_reference()

    if not app_reference.child(key).get():
        data = {}
    else:
        data = app_reference.child(key).get()
    
    delete_app()

    return data
        
def write_data(key:str, value:str) -> None:

    app_reference: Reference = get_app_reference()

    if app_reference.child(key).get() is not None:
        print(f"Key '{key}' exists in the database.")
    else:
        app_reference.child(key).set(value)
        print('Data written successfully!')
    
    delete_app()

def update_data(key:str, value:str) -> None:
    
    app_reference: Reference = get_app_reference()

    if app_reference.child(key).get() is not None:
        app_reference.child(key).set(value)
        print(f"Key '{key}' has been updated.")
    else:
        print(f"Key '{key}' does not exist in the database.")
        
    delete_app()

def add_idee(identifiant:str, value:str) -> None:

    app_reference: Reference = get_app_reference()
    key = identifiant + 'cadeau'
    
    if app_reference.child(key).get() == "Pas d'idées de cadeau pour le moment! 😭":
        app_reference.child(key).set("Idée : " + value)
        
    elif app_reference.child(key).get() != "Pas d'idées de cadeau pour le moment! 😭":
        data = app_reference.child(key).get()
        app_reference.child(key).set(data + ",   " + value)

    delete_app()

def delete_data(key:str) -> None:
    
        app_reference: Reference = get_app_reference()
    
        if app_reference.child(key).get() is not None:
            app_reference.child(key).delete()
            print(f"Key '{key}' has been deleted.")
        else:
            print(f"Key '{key}' does not exist in the database.")
        
        delete_app()

def delete_all_data() -> None:
    
    app_reference: Reference = get_app_reference()
    
    app_reference.delete()
    
    delete_app()


## Tirer au sort un membre de la famille parmi ceux restants

def initiate_secret_santa_data() -> None:

    delete_all_data()

    family = pd.read_csv(FAMILY_PATH)

    for index, row in family.iterrows():
        write_data(row['identifiant'] + 'cadeau', "Pas d'idées de cadeau pour le moment! 😭")
        write_data(row['identifiant'] + 'tirage', "")
        write_data(row['identifiant'] + 'est_deja_tire', "non")
        write_data(row['identifiant'] + 'a_tire', "non")

def tirage(identifiant):

    family = pd.read_csv(FAMILY_PATH)
    # si la personne a deja tire : impossible de retirer 
    if get_data(identifiant + 'a_tire') == "oui":
        return get_data(identifiant+'tirage')
    
    if get_data(identifiant + 'a_tire') == "non":
        personnes_restantes = []
        for index, row in family.iterrows():
            if get_data(row['identifiant'] + 'est_deja_tire') == "non":
                personnes_restantes.append(row['identifiant'])
        identifiant_tire = random.choice(personnes_restantes)

        update_data(identifiant + 'tirage', identifiant_tire)
        update_data(identifiant + 'a_tire', "oui")
        update_data(identifiant_tire + 'est_deja_tire', "oui")
        return identifiant_tire

def get_tirage_idee(identifiant):
    tirage = get_data(identifiant + 'tirage')

    cadeaux = get_data(tirage + 'cadeau')
    
    return cadeaux


from unidecode import unidecode
    
def clean(text: str):
    return unidecode(text.lower())
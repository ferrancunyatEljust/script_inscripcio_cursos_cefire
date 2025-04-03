from datetime import datetime
import re

mesos = {
    "gener": 1, "febrer": 2, "març": 3, "abril": 4, "maig": 5,
    "juny": 6, "juliol": 7, "agost": 8, "setembre": 9,
    "octubre": 10, "novembre": 11, "desembre": 12
}

def parse_data_catala(data_text):
    pattern = r"(\d{1,2})\s+d['e]\s*([a-zàéèíòóúç]+)\s+de\s+(\d{4})"
    match = re.match(pattern, data_text.strip(), re.IGNORECASE)
    
    if not match:
        raise ValueError(f"No s'ha pogut interpretar la data: '{data_text}'")

    dia = int(match.group(1))
    nom_mes = match.group(2).lower()
    any_ = int(match.group(3))

    mes = mesos.get(nom_mes)
    if not mes:
        raise ValueError(f"Mes desconegut: '{nom_mes}'")

    return datetime(any_, mes, dia)

import json


def read_json(file_name: str) -> dict:
    """
    Lit un fichier json et le retourne sous forme de dictionnaire.
    :param file_name:
    :return: Un dictionnaire contenant le contenu du fichier
    """
    try:
        with open(file_name, "r") as file:
            return json.load(file)
    except FileNotFoundError as e:
        print(f"Erreur: Le fichier {file_name} n'a pas été trouvé.")
        raise e

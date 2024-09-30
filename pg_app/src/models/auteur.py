from pg_app.src.models.entity import Entity


class Auteur(Entity):
    """
    Classe qui represente un auteur
    """

    auteur_list: list = []

    def __init__(self, nom: str, biographie: str):
        self._id = None
        self.nom = nom
        self.biographie = biographie

        Auteur.auteur_list.append(self)

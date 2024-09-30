from pg_app.src.models.entity import Entity


class Editeur(Entity):
    """
    Classe qui represente un editeur
    """

    editor_list: list = []

    def __init__(self, nom: str):
        self._id = None
        self.nom = nom

        Editeur.editor_list.append(self)

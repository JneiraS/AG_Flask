from pg_app.src.models.entity import Entity


class MembreJury(Entity):
    """
    Classe qui represente un membre du jury
    """

    def __init__(self, nom: str, role: str):
        self._id = None
        self.nom = nom
        self.role = role

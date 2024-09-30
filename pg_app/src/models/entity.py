from abc import ABC, abstractmethod


class Entity(ABC):
    """
    Interface pour les entités du modèle.
    """

    @abstractmethod
    def __init__(self):
        self._id = None

    @property
    def id(self):
        """Identifiant unique de l'entité."""
        return self._id

    @id.setter
    def id(self, value):
        """
        Définit l'identifiant unique de l'entité.
        """
        if not isinstance(value, (int, type(None))):
            raise ValueError("id doit être un entier ou None")
        self._id = value

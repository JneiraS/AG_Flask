from enum import Enum


class TableName(Enum):
    """
    Nom des tables de la base de données.
    """

    LIVRES = "livres"
    AUTEURS = "auteurs"
    EDITEURS = "editeurs"
    MEMBER_JURY = "membre_jury"
    PERSONNAGES = "personnages"
    EDIT = "edit"
    ECRIT = "ecrit"
    APPARTIENT = "appartient"
    VOTE = "vote"

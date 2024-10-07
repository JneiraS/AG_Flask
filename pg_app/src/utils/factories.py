#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ce fichier contient la classe Creator qui s'occupe de la creation d'objets.
"""

import concurrent.futures
from abc import ABC, abstractmethod

from pg_app.src.dao.auteurs_dao import AuteursDAO
from pg_app.src.dao.base_dao import DatabaseConnectionManager
from pg_app.src.dao.ecrit_dao import EcritDAO
from pg_app.src.dao.edit_dao import EditDAO
from pg_app.src.dao.editeurs_dao import EditeursDAO
from pg_app.src.dao.livres_dao import LivresDAO
from pg_app.src.dao.membre_jury_dao import MembresJuryDAO
from pg_app.src.dao.personnages_dao import PersonnagesDAO
from pg_app.src.models.auteur import Auteur
from pg_app.src.models.editeur import Editeur
from pg_app.src.models.livre import Livre
from pg_app.src.models.membre_jury import MembreJury
from pg_app.src.models.personnage import Personnage


class Creator(ABC):

    @abstractmethod
    def factory_method(self, information_source) -> None:
        """
        Méthode abstraite qui doit être implémentée.
        Cette méthode prend une source d'information en entrée et créer un nouvel objet.
        :param information_source:
        :return:
        """
        pass


class LivresCreator(Creator):

    def factory_method(self, information_source: dict) -> Livre:
        """
        Methode qui retourne un nouvel objet Person.
        :param information_source:
        """
        livre: Livre = Livre(
            information_source["titre"],
            information_source["resume"],
            information_source["date_parution"],
            information_source["nombre_pages"],
            information_source["ISBN"],
            information_source["prix"],
        )

        livre._id = information_source["id_livre"]

        return livre


class AuteursCreator(Creator):

    def factory_method(self, information_source: dict) -> Auteur:
        """
        Methode qui retourne un nouvel objet Auteur.
        :param information_source:
        """
        auteur: Auteur = Auteur(
            information_source["nom"],
            information_source["biographie"],
        )

        auteur._id = information_source["id_auteur"]

        return auteur


class EditeursCreator(Creator):

    def factory_method(self, information_source: dict) -> Editeur:
        """
        Methode qui retourne un nouvel objet Editeur.
        :param information_source:
        """
        editeur: Editeur = Editeur(
            information_source["nom"],
        )

        editeur._id = information_source["id_editeur"]

        return editeur


class MembreJuryCreator(Creator):

    def factory_method(self, information_source: dict) -> MembreJury:
        """
        Methode qui retourne un nouvel objet MembreJury.
        :param information_source:
        """
        membre_jury: MembreJury = MembreJury(
            information_source["nom"],
            information_source["role"],
        )

        membre_jury._id = information_source["id_membre"]

        return membre_jury


class PersonnagesCreator(Creator):

    def factory_method(self, information_source: dict) -> Personnage:
        """
        Methode qui retourne un nouvel objet Personnages.
        :param information_source:
        """
        personnages: Personnage = Personnage(
            information_source["nom"],
            information_source["role"],
        )

        personnages._id = information_source["id_personnage"]

        return personnages


def get_all_entities(class_dao: DatabaseConnectionManager) -> list[dict]:
    """
    Récupère tous les enregistrements de la table de la base de données
    associée à cette instance de DatabaseConnectionManager.
    :param class_dao: un objet de type DatabaseConnectionManager
    :return:  list[dict] : Une liste de dictionnaires, où chaque dictionnaire
    represente un enregistrement dans la table de la base de données.
    """
    entity = class_dao
    return entity.get_all()


def add_attribute_to_livres_from_database(
    attribute_name: str, dao_class, get_method: callable
) -> None:
    """
    Ajoute un attribut spécifié à toutes les instances de livre.

    Cette fonction prend en paramètre le nom de l'attribut à ajouter, la classe du DAO à utiliser,
    et la méthode à appeler sur l'instance DAO pour récupérer la valeur de l'attribut.
    Elle utilise ensuite l'instance DAO pour récupérer les valeurs de l'attribut pour chaque instance de livre
    et définit l'attribut sur l'instance de livre en utilisant la fonction setattr.
    """
    dao_instance = dao_class()
    livres = Livre.book_list

    for livre in livres:
        setattr(livre, attribute_name, get_method(dao_instance, livre.id))


def create_all_personnages_from_database() -> list[Personnage]:
    """Creer tous les personnages de la base de données."""
    return list(
        map(PersonnagesCreator().factory_method, get_all_entities(PersonnagesDAO()))
    )


def create_all_membre_jury_from_database() -> list[MembreJury]:
    """Creer tous les membres du jury de la base de données."""
    return list(
        map(MembreJuryCreator().factory_method, get_all_entities(MembresJuryDAO()))
    )


def create_all_editeurs_from_database() -> list[Editeur]:
    """Creer tous les editeurs de la base de données."""
    return list(map(EditeursCreator().factory_method, get_all_entities(EditeursDAO())))


def create_all_livres_from_database() -> list[Livre]:
    """Creer tous les livres de la base de données."""
    return list(map(LivresCreator().factory_method, get_all_entities(LivresDAO())))


def create_all_auteurs_from_database() -> list[Auteur]:
    """Creer tous les auteurs de la base de données."""
    return list(map(AuteursCreator().factory_method, get_all_entities(AuteursDAO())))


def initialize_database_in_threads() -> None:
    """
    Initialise la base de données en créant tous les objets auteur, editeur, livre, membre_jury et personnage
    et en ajoutant les editeurs et auteurs aux livres en utilisant des threads.
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(create_all_auteurs_from_database)
        executor.submit(create_all_editeurs_from_database)
        executor.submit(create_all_livres_from_database)
        executor.submit(create_all_membre_jury_from_database)
        executor.submit(create_all_personnages_from_database)

    add_attribute_to_livres_from_database(
        "editeur",
        EditDAO,
        lambda dao, identifier: dao.get_editeur_name_by_livre_id(identifier),
    )
    add_attribute_to_livres_from_database(
        "auteur",
        EcritDAO,
        lambda dao, identifier: dao.get_auteur_by_livre_id(identifier),
    )

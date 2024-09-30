#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ce fichier contient la classe Creator qui s'occupe de la creation d'objets.
"""

import concurrent.futures
from abc import ABC, abstractmethod

from pg_app.src.dao.auteurs_dao import AuteursDAO
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


def create_all_personnages_from_database() -> list[Personnage]:
    """
    Creer tous les personnages de la base de données.
    """
    personnages = PersonnagesDAO()
    results: list[dict] = personnages.get_all()
    return list(map(PersonnagesCreator().factory_method, results))


def create_all_membre_jury_from_database() -> list[MembreJury]:
    """
    Creer tous les membres du jury de la base de données.
    """
    membre_jury = MembresJuryDAO()
    results: list[dict] = membre_jury.get_all()
    return list(map(MembreJuryCreator().factory_method, results))


def create_all_editeurs_from_database() -> list[Editeur]:
    """
    Creer tous les editeurs de la base de données.
    """
    editeurs = EditeursDAO()
    results: list[dict] = editeurs.get_all()
    return list(map(EditeursCreator().factory_method, results))


def create_all_livres_from_database() -> list[Livre]:
    """
    Creer tous les livres de la base de données.
    """
    livres = LivresDAO()
    results: list[dict] = livres.get_all()
    return list(map(LivresCreator().factory_method, results))


def create_all_auteurs_from_database() -> list[Auteur]:
    """
    Creer tous les auteurs de la base de données.
    """
    auteurs = AuteursDAO()
    results: list[dict] = auteurs.get_all()
    return list(map(AuteursCreator().factory_method, results))


def add_editor_to_livres_from_database() -> None:
    """
    Ajoute un editeur à toutes les instance de livre"""
    editeurs = EditDAO()
    livres = Livre.book_list

    for livre in livres:
        livre.editeur = editeurs.get_editeur_name_by_livre_id(livre.id)


def add_auteur_to_livres_from_database() -> None:
    """
    Ajoute un auteur à toutes les instance de livre"""
    auteurs = EcritDAO()
    livres = Livre.book_list

    for livre in livres:
        livre.auteur = auteurs.get_auteur_by_livre_id(livre.id)


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

    add_editor_to_livres_from_database()
    add_auteur_to_livres_from_database()

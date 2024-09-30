#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ce fichier contient la classe DatabaseConnectionManager qui s'occupe d'ouvrir et de fermer les
connexions a la base de donnees. Il contient aussi une classe abstraite SingletonMeta qui permet de
transformer une classe en singleton.
"""

from threading import Lock

import pymysql

from pg_app.src.utils.logger import logger, LogMessages
from contextlib import contextmanager

class SingletonMeta(type):
    """
    Permet de transformer une classe en singleton.
    """

    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class DatabaseConnectionManager(metaclass=SingletonMeta):
    """
    Classe qui s'occupe d'ouvrir et de fermer les connexions a la base de  données.
    """

    def __init__(self, table_name: str):
        self.table_name = table_name
        self.conn = None
        self.cursor = None

    def open_connection(self) -> None:
        """
        Ouvre une connexion a la base de données.

        Ouvre un fichier de configuration JSON et lit les informations de connexion a la base de données.
        Si le fichier n'existe pas, un message d'erreur est imprimé et une exception FileNotFoundError est
        levée. Si le fichier existe, une connexion à la base de donnees est établie et un curseur est cree.
        """
        config = None
        try:
            config = {
                "host": "localhost",
                "user": "jneira",
                "password": "pp&P&Tpa",
                "db": "goncourt"
            }
        except FileNotFoundError as e:
            print(f"An error occurred: {e}")
            logger.error(f"{LogMessages.FILE_NOT_FOUND.value}{str(e)}")

        if config is not None:
            self.conn = pymysql.connect(
                **config, cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.conn.cursor()
        else:
            logger.error("Failed to read database configuration")

    def close_connection(self) -> None:
        """
        Ferme la connexion avec la base de données.
        Ferme le curseur et la connexion associés si ils existent.
        """

        if self.cursor:
            self.cursor.close()

    def get_all(self, limit: int = None, offset: int = None) -> list[dict]: 
        """
        Récupère tous les enregistrements de la table de la base de données associée à cette instance de
        DatabaseConnectionManager.
        :param limit: Nombre maximal d'enregistrements à renvoyer. La valeur par défaut est None.
        :param offset: Le nombre d'enregistrements à sauter avant de commencer à renvoyer des enregistrements.
        La valeur par défaut est None.
        :return: list[dict] : Une liste de dictionnaires, où chaque dictionnaire représente un
        enregistrement dans la table de la base de données.
        """
        query = f"SELECT * FROM {self.table_name}"
        params = []

        if limit is not None:
            query += f" LIMIT {limit}"
            params.append(limit)

        if offset is not None:
            query += f" OFFSET {offset}"
            params.append(offset)

        results: list[dict] = self.query_database(query)
        return results

    def create(self, query) -> int | None:
        """
        Crée une nouvelle entité dans la base de données et retourne son identifiant.
        :param query:
        """
        return self.insert_and_get_id(query)

    def read(self, identifier: int = None) -> list[dict] | None:
        """
        Récupère une entité dans la base de données selon son identifiant
        :param identifier:
        """
        query = f"SELECT * FROM {self.table_name} WHERE id_membre = {identifier}"
        return self.query_database(query)

    def update(self, table) -> bool:
        """
        Met à jour une entité dans la base de données.
        :param table:
        """
        pass

    def delete(self, id_to_delete: int) -> bool:
        """
        Supprime une entité dans la base de données, grace à son identifiant.
        :param id_to_delete:
        :return:
        """

        query = f"DELETE FROM {self.table_name} WHERE id = {id_to_delete}"
        if self.run_query_with_commit(query):
            return True
        return False
    

    @contextmanager
    def get_connection(self):
        conn = None
        try:
            conn = self.create_connection()  # Méthode pour créer une nouvelle connexion
            yield conn
        finally:
            if conn and conn.open:
                conn.close()

    def query_database(self, query, params=None):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
        return result






    def insert_and_get_id(self, query: str) -> int | None:
        """
        Insère une nouvelle valeur dans la base de données et retourne son identifiant.
        :param self:
        :param query:  La requête SQL
        :return: identifiant de la nouvelle entité
        """
        logger.debug(LogMessages.DEBUG_MESSAGE.value)
        try:
            self.open_connection()
            self.cursor.execute(query)
            id_generated = self.cursor.lastrowid
            self.conn.commit()
            logger.info(LogMessages.SUCCESS_QUERY_MESSAGE.value)

            return id_generated

        except Exception as e:
            print(f"Une erreur est survenue : {e}")
            logger.error(f"{LogMessages.ERRUER_MESSAGE.value}{str(e)}")
            return None
        
        finally:
            if self.conn:
                self.conn.close()

    def query_database(self, query: str) -> list[dict] | None:
        """
        Exécute une requête SQL et renvoie les résultats sous forme de liste de dictionnaires.
        :param self:
        :param query: la requête SQL
        :return: liste de dictionnaires ou None
        """
        logger.debug(LogMessages.DEBUG_MESSAGE.value)
        try:
            self.open_connection()
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            logger.info(LogMessages.SUCCESS_QUERY_MESSAGE.value)

            return rows

        except Exception as e:
            print(f"Une erreur est survenue : {e}")
            logger.error(f"{LogMessages.ERRUER_MESSAGE.value}{str(e)}")
            return None
        
        finally:
            if self.conn and self.conn.open:
                self.conn.close()

    def run_query_with_commit(self, query: str):
        """
        Exécute une requête SQL et valide la transaction.
        :param self:
        :param query: la requête SQL
        :return: True si la requête a été exécutée correctement, False sinon
        """
        logger.debug(LogMessages.DEBUG_MESSAGE.value)

        try:
            self.open_connection()
            self.cursor.execute(query)
            self.conn.commit()
            logger.info(LogMessages.SUCCESS_QUERY_MESSAGE.value)

            return True

        except Exception as e:
            print(f"An error occurred: {e}")
            logger.error(f"{LogMessages.ERRUER_MESSAGE.value}{str(e)}")
            self.close_connection()
            return False
        
        finally:
            if self.conn:
                self.conn.close()

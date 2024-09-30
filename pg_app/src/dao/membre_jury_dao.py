from pg_app.src.dao.base_dao import DatabaseConnectionManager

from pg_app.src.utils.tables_names import TableName


class MembresJuryDAO(DatabaseConnectionManager):
    """
    Classe qui s'occupe de la table membre_jury.
    """

    def __init__(self, table_name: str = TableName.MEMBER_JURY.value):
        super().__init__(table_name)
        self.table_name = table_name

    def gethash(self, hash_password: str) -> dict | None:
        """
        Récupère un membre de la table membre_jury en fonction de son mot de passe.
        :param hash_password: Le mot de passe de l'utilisateur.
        :return: list[dict] : Une liste de dictionnaires, où chaque dictionnaire spécente un
        """
        query = f"SELECT id_membre FROM {self.table_name} WHERE mot_de_passe = '{hash_password}'"
        results: list[dict] = self.query_database(query)

        if results == ():
            return None

        return results[0]

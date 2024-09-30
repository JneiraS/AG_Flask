from pg_app.src.dao.base_dao import DatabaseConnectionManager
from pg_app.src.models.livre import Livre

from pg_app.src.utils.tables_names import TableName


class AppartientDAO(DatabaseConnectionManager):
    """
    Classe qui s'occupe de la table appartient.
    """

    def __init__(self, table_name: str = TableName.APPARTIENT.value):
        super().__init__(table_name)
        self.table_name = table_name

    def get_selection(self, selection: int) -> list[dict]:
        query: str = (
            f"SELECT * FROM `{TableName.APPARTIENT.value}` WHERE `id_selection` = {selection}"
        )
        results: list[dict] = self.query_database(query)
        return results

    def get_books_in_selection(self, selection: int) -> list[Livre]:
        """
        Récupère tous les livres d'une sélection spécifique.

        Cette méthode utilise l'objet DAO Appartient pour obtenir les livres
        associés à une sélection donnée et les retourne sous forme de liste.
        :param selection: l'identifiant de la selection
        :return:
        """
        second_selection_list: list = []
        results: list[dict] = self.get_selection(selection)
        for result in results:
            for book in Livre.book_list:
                if result["id_livre"] == book.id:
                    second_selection_list.append(book)
        return second_selection_list

    def insert_book_to_selection(self, id_livre: int, id_selection: int):
        """
        Insère un livre dans une collection spécifique.
        Cette méthode utilise l'objet DAO Appartient pour insérer une entrée
        dans la table.

        :param id_livre:
        :param id_selection:
        """
        return self.create(
            f"INSERT INTO `{TableName.APPARTIENT.value}` (`id_livre`, `id_selection`) VALUES "
            f"('{id_livre}', '{id_selection}')"
        )

    def add_books_to_selection(
        self, selection_id: int, results_list: list[int]
    ) -> bool:
        """
        Ajoute tous les livres d'une liste à une selection.

        Cette méthode utilise la liste d'identifiants de livres créée par
        `list_maker()` et les ajoute à la sélection spécifiée.
        :param results_list: la liste d'identifiants de livres
        :param selection_id: l'identifiant de la selection
        :return:
        """

        for book in results_list:
            if self.insert_book_to_selection(book, selection_id) is None:
                return False
            else:
                continue
        return True

    def get_current_round(self) -> int:
        """
        Methode qui permet de connaitre le tour actuel en cours.
        Si la table est vide, alors le tour actuel est le premier, sinon
        il prend la valeur du maximum des identifiants de selection.
        """

        if self.query_database(f"SELECT * FROM {self.table_name} WHERE 1") == ():
            return 1
        else:
            r = self.query_database(f"SELECT MAX(id_selection) FROM {self.table_name}")[
                0
            ]
            return r["MAX(id_selection)"]

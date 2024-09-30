from pg_app.src.dao.base_dao import DatabaseConnectionManager
from pg_app.src.models.auteur import Auteur
from pg_app.src.utils.tables_names import TableName


class EcritDAO(DatabaseConnectionManager):
    """
    Classe qui s'occupe de la table livres.
    """

    def __init__(self, table_name: str = TableName.ECRIT.value):
        super().__init__(table_name)
        self.table_name = table_name

    def get_auteur_by_livre_id(self, livre_id: int) -> str:
        """
        Récupère l'auteur d'un livre dans la base de données.
        """

        ecrit_table = self.get_all()

        for ecrit in ecrit_table:
            if ecrit["id_livre"] == livre_id:
                for auteur in Auteur.auteur_list:
                    if ecrit["id_auteur"] == auteur.id:
                        return auteur.nom

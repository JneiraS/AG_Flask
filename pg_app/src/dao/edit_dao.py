from pg_app.src.dao.base_dao import DatabaseConnectionManager
from pg_app.src.models.editeur import Editeur
from pg_app.src.utils.tables_names import TableName


class EditDAO(DatabaseConnectionManager):
    """
    Classe qui s'occupe de la table edit.
    """

    def __init__(self, table_name: str = TableName.EDIT.value):
        super().__init__(table_name)
        self.table_name = table_name

    def get_editeur_name_by_livre_id(self, livre_id: int) -> str:
        """
        Récupère le nom de l'editeur d'un livre.
        :param livre_id:
        :return:
        """
        edit_table = self.get_all()

        for edit in edit_table:
            if edit["id_livre"] == livre_id:
                for editeur in Editeur.editor_list:
                    if edit["id_editeur"] == editeur.id:
                        return editeur.nom

        return ""

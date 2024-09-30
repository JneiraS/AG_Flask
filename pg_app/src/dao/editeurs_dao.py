from pg_app.src.dao.base_dao import DatabaseConnectionManager
from pg_app.src.utils.tables_names import TableName


class EditeursDAO(DatabaseConnectionManager):
    """
    Classe qui s'occupe de la table livres.
    """

    def __init__(self, table_name: str = TableName.EDITEURS.value):
        super().__init__(table_name)
        self.table_name = table_name

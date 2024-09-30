from pg_app.src.dao.base_dao import DatabaseConnectionManager
from pg_app.src.utils.tables_names import TableName


class VoteDAO(DatabaseConnectionManager):
    """
    Classe qui s'occupe de la table auteurs.
    """

    def __init__(self, table_name: str = TableName.VOTE.value):
        super().__init__(table_name)
        self.table_name = table_name

    def get_voting_results_for(
        self, round_vote: int, length_of_selection: int
    ) -> list[dict] | None:
        """
        Renvoie les résultats de vote pour une tour de vote donnée.
        :param length_of_selection: taille de la selection
        :param round_vote: l'identifiant de la ronde de vote
        :return: la liste des identifiants des livres qui ont  t  choisis
        """

        if round_vote == 1:
            return self.query_database(
                f"SELECT * FROM {TableName.LIVRES.value} WHERE 1;"
            )

        else:
            return self.query_database(
                f"SELECT id_livre, COUNT(*) AS nombre_de_votes FROM {self.table_name} WHERE "
                f"id_selection={round_vote} GROUP BY id_livre ORDER BY nombre_de_votes DESC LIMIT"
                f" {length_of_selection}")



    def has_voted(self, id_member: int, round_vote: int) -> bool:
        """
        Vérifie si un membre a voté dans le tour actuel.
        :param id_member: Identifiant unique du membre.
        :param round_vote: Selection actuel.
        :return: True si le membre a voté, False sinon.
        """
        return (
            self.query_database(
                f"SELECT * FROM {self.table_name} WHERE `id_membre` = {id_member} AND "
                f"`id_selection` = {round_vote + 1}"
            )
            == ()
            and round_vote < 3
        )

    def send_all_votes_to_db(self, choices: list, id_member: int, vote_round: int):
        """
        Enregistre les votes dans la base de données.
        :param choices: Nombre de livres que le membre a choisi
        :param id_member: Identifiant unique du membre
        :param vote_round: Tour actuel
        :return:
        """
        coef: int = len(choices)

        for choice in choices:
            for _ in range(coef):
                self.create(
                    f"INSERT INTO `{self.table_name}` (`id_vote`,`id_livre`, `id_membre`, `id_selection`) "
                    f"VALUES ("
                    f"NULL,{choice},{id_member},{vote_round + 1})"
                )
            coef -= 1

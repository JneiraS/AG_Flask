from ..src.dao.appartient_dao import AppartientDAO
from ..src.dao.vote_dao import VoteDAO
from .. import Livre




def confirm_vote(results_list: list[int]):
    """
    Ajoute tous les livres d'une liste à une selection.

    :param results_list:
    :return:
    """
    dao_appartient = AppartientDAO()
    current_round = dao_appartient.get_current_round()
    print(f" tour actuel: {current_round}")

    for book in results_list:
        if dao_appartient.insert_book_to_selection(book, current_round + 1) is None:
            return False
        else:
            continue
    return True


def render_votes_results(round_vote: int, length_of_selection: int) -> list[dict]:
    """Renvoie les résultats des votes pour une sélection."""
    dao_vote = VoteDAO()
    vote_results = dao_vote.get_voting_results_for(round_vote, length_of_selection)
    books = Livre.book_list

    for result in vote_results:
        for book in books:
            if result["id_livre"] == book.id:
                result["title"] = book.title
                break

    return vote_results
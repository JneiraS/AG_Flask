from pg_app.src.models.livre import Livre
from ..src.dao.appartient_dao import AppartientDAO
from ..src.dao.vote_dao import VoteDAO


def confirm_vote(results_list: list[int]):
    """
    Ajoute tous les livres d'une liste à une selection.

    :param results_list:
    :return:
    """
    dao_appartient = AppartientDAO()
    current_round = dao_appartient.get_current_round()

    for book in results_list:
        if dao_appartient.insert_book_to_selection(book, current_round + 1) is None:
            return False
        else:
            continue
    return True


def render_votes_results(round_vote: int, selection_length: int) -> list[dict]:
    """Renvoie les résultats de vote pour un tour de vote donnée."""
    vote_dao = VoteDAO()
    all_books = Livre.book_list
    voting_results = vote_dao.get_voting_results_for(round_vote, selection_length)

    add_titles_to_voting_results(all_books, voting_results)

    return voting_results


def add_titles_to_voting_results(all_books, voting_results):
    """Itère sur les résultats de vote et ajoute les titres des livres"""
    for result in voting_results:
        book = next((book for book in all_books if book.id == result["id_livre"]), None)
        if book:
            result["title"] = book.title

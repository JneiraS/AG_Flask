from pg_app import Livre
from pg_app.src.dao.appartient_dao import AppartientDAO
from pg_app.src.dao.base_dao import DatabaseConnectionManager
from pg_app.src.dao.livres_dao import LivresDAO
from pg_app.src.utils.factories import get_all_entities


def book_to_dict(book) -> dict:
    """Convertit un objet Livre en un dictionnaire structuré."""
    data = {
        "title": book.title,
        "summary": book.summary,
        "publication_date": book.publication_date,
        "number_of_pages": book.number_of_pages,
        "isbn": book.isbn,
        "price": book.price,
    }
    return data


def find_book_by(attr, value):
    """Recherche un livre dans la liste des livres en fonction
    d'un attribut spécifique et de sa valeur."""
    return next(
        (book for book in Livre.book_list if getattr(book, attr) == value), None
    )


def get_books_in_selection(selection):
    """Récupère la liste des livres associés à une sélection donnée."""
    appartient_dao = AppartientDAO()
    return appartient_dao.get_books_in_selection(selection)


# ---json-server--- #


def dao_to_dict():

    books: dict = get_entities_as_dict(LivresDAO(), "books")
    return books


def get_entities_as_dict(dao: DatabaseConnectionManager, key: str) -> dict:
    """Récupère toutes les entités de la table de la base de données du DAO donné et les organise dans un dictionnaire."""
    entities = get_all_entities(dao)
    return {key: entities}

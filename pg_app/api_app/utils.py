from pg_app import Livre


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
    return next((book for book in Livre.book_list if getattr(book, attr) == value), None)

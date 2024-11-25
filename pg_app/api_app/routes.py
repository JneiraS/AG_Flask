from flask import (
    jsonify
)

from slugify import slugify

from . import bp
from .. import Livre


@bp.route('/books', methods=["GET"])
def get_all_books():
    """Return a JSON object of all books."""
    books = {book.title: book_to_dict(book) for book in Livre.book_list}
    return jsonify({"books": books})


@bp.route('/books/<int:book_id>', methods=["GET"])
def get_book(book_id):
    """Retourne un objet JSON du livre avec l'ID donné."""
    selected_book = next((book for book in Livre.book_list if book.id == book_id), None)
    if not selected_book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify({"book": book_to_dict(selected_book)})


@bp.route('/books/<string:title>', methods=["GET"])
def get_book_by_title(title):
    """Retourne un objet JSON du livre avec le titre donné."""
    # TODO comparere des slugs
    matching_book = next((book for book in Livre.book_list if slugify(book.title) == slugify(title)), None)
    if matching_book is None:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify({'book': book_to_dict(matching_book)})


# TODO Déplacer dans un fichier  utils
def book_to_dict(book) -> dict:
    data = {book.title: {
        "id": book.id,
        "summary": book.summary,
        "publication_date": book.publication_date,
        "number_of_pages": book.number_of_pages,
        "isbn": book.isbn,
        "price": book.price,
    }}
    return data

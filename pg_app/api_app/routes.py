import datetime

from flask import (
    jsonify, Response, request
)
from slugify import slugify

from pg_app.src.dao.appartient_dao import AppartientDAO
from pg_app.src.models.livre import Livre
from . import bp
from .utils import find_book_by, book_to_dict, get_books_in_selection
from ..src.dao.membre_jury_dao import MembresJuryDAO


@bp.route('/books', methods=["GET"])
def get_all_books():
    """Retourne un objet JSON avec tous les livres."""
    books = {book.id: book_to_dict(book) for book in Livre.book_list}
    return jsonify({"books": books})


@bp.route('/books/<int:book_id>', methods=["GET"])
def get_book(book_id):
    """Retourne un objet JSON du livre avec l'ID donné."""
    selected_book = find_book_by("id", book_id)
    if not selected_book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify({"book": book_to_dict(selected_book)})


@bp.route('/books/<string:title>', methods=["GET"])
def get_book_by_title(title) -> tuple[Response, int] | Response:
    """Retourne un objet JSON du livre avec le titre donné."""
    matching_book = find_book_by("slug", slugify(title))
    if matching_book is None:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify({'book': book_to_dict(matching_book)})


@bp.route('/selection/<int:selection>')
def get_date_and_selection_books(selection: int) -> Response:
    """Retourn  un objet JSON avec toutes les informations des
     livres d'une sélection donné"""
    books_selection = get_books_in_selection(selection)
    books = {book.title: book_to_dict(book) for book in books_selection}
    return jsonify({"books": books, "date": datetime.datetime(2012, 12, 12).isoformat()})


@bp.route('/selection/<int:selection>/books')
def get_list_of_titles_books(selection: int):
    """Retourn  un objet JSON  avec une liste des livres d'une
    sélection donné """
    books_selection: list[Livre] = get_books_in_selection(selection)
    title_books = [book.title for book in books_selection]
    return jsonify({f"books in selection {selection}": title_books})


@bp.route('/selection/<int:selection>/books_id')
def get_list_of_ids_books(selection: int):
    """Retourn  un objet JSON  avec une liste des id des livres d'une
    sélection donné """
    books_selection = get_books_in_selection(selection)
    ids_books = [book.id for book in books_selection]
    return jsonify({f"books in selection {selection}": ids_books})


@bp.route('/selection/<int:selection_id>', methods=["POST"])
def add_book_to_selection(selection_id: int) -> tuple[Response, int]:
    """Add books to a selection."""
    dao = AppartientDAO()
    member_dao = MembresJuryDAO()

    data = request.get_json()
    if (user_id := data.get("auth")) is None:
        return jsonify({"error": "Missing auth"}), 400
    if not isinstance((book_ids := data.get("book_ids")), list):
        return jsonify({"error": "Book ids must be a list"}), 400

    if not member_dao.gethash(user_id):
        return jsonify({"error": "You don't have permission to do that"}), 400

    if not dao.add_books_to_selection(selection_id, book_ids):
        return jsonify({"error": "Failed to add book to selection"}), 400

    return jsonify({"message": "Book added successfully"}), 201

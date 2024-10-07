# -*- coding: utf-8 -*-
from flask import Flask, render_template

from pg_app.src.models.editeur import Editeur
from pg_app.src.models.livre import Livre
from pg_app.src.utils.factories import initialize_database_in_threads
from . import auth_app
from . import member_app
from .src.dao.appartient_dao import AppartientDAO
from .src.models.livre import Livre


def create_app():
    """
    Fonction qui permet de creer l'application
    """
    app = Flask(__name__)

    app.secret_key = "U2FsdGVkX1+H7ODzq10448prts5ZjZs0zYZyQwNzv2ClgXQH8hwXiZ8y4BRryyC3"

    initialize_database_in_threads()
    app.register_blueprint(auth_app.bp)
    app.register_blueprint(member_app.bp)

    @app.route("/")
    def home():
        list_of_selected_books = Livre.book_list
        list_of_editors = Editeur.editor_list
        return render_template(
            "index.html", livres=list_of_selected_books, editors=list_of_editors
        )

    @app.route("/seconde-selection")
    def seconde_selection():
        appartient_dao = AppartientDAO()
        seconde_selection_list: list[Livre] = appartient_dao.get_books_in_selection(2)

        return render_template("index.html", livres=seconde_selection_list)

    @app.route("/troisieme-selection")
    def troisieme_selection():
        appartient_dao = AppartientDAO()
        troisieme_selection_list: list[Livre] = appartient_dao.get_books_in_selection(3)

        return render_template("index.html", livres=troisieme_selection_list)

    return app

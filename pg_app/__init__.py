from flask import Flask, render_template

from pg_app.src.utils.factories import initialize_database_in_threads
from pg_app.src.models.livre import Livre
from pg_app.src.models.editeur import Editeur

from . import auth
from . import blog


def create_app():
    app = Flask(__name__)

    initialize_database_in_threads()
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    @app.route("/")
    def home():
        list_of_selected_books = Livre.book_list
        list_of_editors = Editeur.editor_list
        return render_template('index.html', livres=list_of_selected_books, editors=list_of_editors)

    return app

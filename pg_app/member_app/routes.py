# -*- coding: utf-8 -*-


from flask import (
    render_template, request
)

from pg_app.auth_app.routes import login_required
from . import bp
from .. import Livre
from ..src.dao.appartient_dao import AppartientDAO
from ..src.dao.vote_dao import VoteDAO
from .froms import RoundvoteRadioForm


@bp.route('/president-menu', methods=['POST', 'GET'])
@login_required
def index():
    """Affiche le menu du président.

    Ce menu permet d'accéder aux différents menus de l'application.
    Il est nécessaire d'être authentifié pour y accéder.
    :return: Le template du menu du président
    """
    form = RoundvoteRadioForm()

    html = 'member/index.html'
    if form.validate_on_submit():
        round_vote = form.round_vote.data
        print(type(round_vote))
        length_of_selection: int = 8 if round_vote == '2' else 4

        vote_results: list[dict] = render_votes_results(int(round_vote), length_of_selection)
        return render_template('%s' % html, results=vote_results, form=form)

    return render_template(html, form=form)


@bp.route('/president-menu/confirmation', methods=['POST'])
@login_required
def fonfirmation():
    """Confirme les résultats affichés"""
    if request.method == 'POST':
        try:
            # Vérifier la confirmation
            confirmation = request.form.get('confirmation')

            if confirmation is not None:
                # Récupérer les résultats du formulaire sous forme de liste de dictionnaires
                id_livres = []

                # Récupérer tous les clés de la MultiDict
                for key in request.form.keys():
                    # Vérifier si la clé correspond à un id_livre
                    if key.startswith('results[') and 'id_livre' in key:
                        # Extraire l'id_livre et l'ajouter à la liste
                        id_livre = request.form[key]
                        id_livres.append(int(id_livre))
                confirm_vote(id_livres)

                return "Confirmation reçue avec les résultats", 200

        except UnicodeDecodeError:
            return "Erreur d'encodage dans les résultats soumis", 400

    return render_template('member/index.html')


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

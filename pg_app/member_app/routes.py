# -*- coding: utf-8 -*-


from flask import (
    render_template, request, redirect, url_for, flash
)

from pg_app.auth_app.routes import login_required
from pg_app.member_app.funcs import confirm_vote, render_votes_results
from pg_app.src.dao.appartient_dao import AppartientDAO
from . import bp
from .froms import RoundvoteRadioForm, DefineWinnerForm


@bp.route('/president-menu', methods=['POST', 'GET'])
@login_required
def index():
    """Affiche le menu du président.

    Ce menu permet d'accéder aux différents menus de l'application.
    Il est nécessaire d'être authentifié pour y accéder.
    :return: Le template du menu du président
    """
    dao_appartient: AppartientDAO = AppartientDAO()
    liste_originale: list[int] = dao_appartient.query_database(
        "SELECT id_livre FROM `appartient` WHERE `id_selection` = 3")
    liste_id = [livre['id_livre'] for livre in liste_originale]
    actual_round: int = dao_appartient.get_current_round()
    form = RoundvoteRadioForm()
    form1 = DefineWinnerForm(liste_id) if actual_round == 3 else None
    html = 'member/index.html'

    if form.validate_on_submit():
        round_vote = form.round_vote.data
        length_of_selection: int = 8 if round_vote == '2' else 4
        vote_results: list[dict] = render_votes_results(int(round_vote), length_of_selection)
        print(vote_results)
        return render_template('%s' % html, results=vote_results, form=form, form1=form1,
                               actual_round=actual_round)

    return render_template(html, form=form, form1=form1, actual_round=actual_round)


@bp.route('/president-menu/confirmation', methods=['POST'])
@login_required
def confirmation():
    """Confirme les résultats affichés"""
    if request.method == 'POST':
        try:
            confirmation = request.form.get('confirmation')

            if confirmation is not None:
                id_livres = []
                # Récupérer tous les clés de la MultiDict
                for key in request.form.keys():
                    # Vérifier si la clé correspond à un id_livre
                    if key.startswith('results[') and 'id_livre' in key:
                        # Extraire l'id_livre et l'ajouter à la liste
                        id_livre = request.form[key]
                        id_livres.append(int(id_livre))
                if confirm_vote(id_livres):
                    flash("Les résultats ont été confirmés et enregistrés avec succès.", "success")
                else:
                    flash("Erreur lors de la confirmation des résultats.", "error")

                return redirect(url_for('president-menu.index'))
        except UnicodeDecodeError:
            return "Erreur d'encodage dans les résultats soumis", 400
    return render_template('member/index.html')


@bp.route('/president-menu/define-winner', methods=['POST'])
def define_winner():
    form1 = DefineWinnerForm()

    if form1.validate_on_submit():
        winner_id = form1.winner.data
        print(winner_id)

    return render_template('member/index.html')

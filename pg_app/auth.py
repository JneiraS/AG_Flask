# -*- coding: utf-8 -*-

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from pg_app.src.dao.membre_jury_dao import MembresJuryDAO
from pg_app.src.utils.auth import Authentication

bp = Blueprint('auth', __name__, url_prefix='/auth')
dao_membre = MembresJuryDAO()


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        password = request.form['password']
        auth_hash: Authentication = (Authentication(password))
        user = dao_membre.gethash(auth_hash.hash_password())

        if user is None:
            error = 'Incorrect username.'

        else:
            session.clear()
            session['user_id'] = user['id_membre']
            return redirect(url_for('president-menu.index'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    """Permet de se deconnecter et d'être redirigé
    vers la page d'accueil
    """
    session.clear()
    return redirect('/')


@bp.before_app_request
def load_logged_in_user():
    """Permet de charger l'utilisateur connecté s'il est connecté."""
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None

    else:
        g.user = dao_membre.read(user_id)[0]


def login_required(view):
    """Décorateur pour vérifier si un utilisateur est connecté  avant d'accéder à une vue.

    Si l'utilisateur n'est pas connecté, il est redirigé vers la page de connexion.
    Sinon, la vue d'origine est appelée.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

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
        print(user)

        if user == ():
            error = 'Incorrect username.'
        else:
            return redirect(url_for('blog.index'))

        flash(error)

    return render_template('auth/login.html')

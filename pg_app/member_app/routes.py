# -*- coding: utf-8 -*-


from flask import (
    render_template, g, redirect, url_for
)

from pg_app.auth import login_required
from . import bp



@bp.route('/president-menu')
@login_required
def index():
    """Affiche le menu du président.

    Ce menu permet d'accéder aux différents menus de l'application.
    Il est nécessaire d'être authentifié pour y accéder.
    :return: Le template du menu du président"""

    # if g.user == None:
    #     return redirect(url_for('auth.login'))

    return render_template('member/index.html')

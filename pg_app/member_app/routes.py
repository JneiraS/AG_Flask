# -*- coding: utf-8 -*-


from flask import (
    render_template
)

from pg_app.auth_app.routes import login_required
from . import bp


@bp.route('/president-menu')
@login_required
def index():
    """Affiche le menu du président.

    Ce menu permet d'accéder aux différents menus de l'application.
    Il est nécessaire d'être authentifié pour y accéder.
    :return: Le template du menu du président"""

    return render_template('member/index.html')

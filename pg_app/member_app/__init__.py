# -*- coding: utf-8 -*-
from flask import Blueprint

bp = Blueprint('president-menu', __name__)
from . import routes

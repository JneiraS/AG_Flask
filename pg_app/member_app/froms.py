from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField


class RoundvoteRadioForm(FlaskForm):
    round_vote = RadioField("Ronde de vote", choices=[(2, "Tour 2"), (3, "Tour 3")])
    submit = SubmitField("Voir les resultats")
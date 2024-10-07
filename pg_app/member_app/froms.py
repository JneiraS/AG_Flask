from flask_wtf import FlaskForm
from wtforms import RadioField, SelectField, SubmitField


class RoundvoteRadioForm(FlaskForm):
    """Formulaire pour la tour de vote."""
    round_vote = RadioField("Ronde de vote", choices=[(2, "Tour 2"), (3, "Tour 3")])
    submit = SubmitField("Voir les resultats")


class DefineWinnerForm(FlaskForm):
    """
    Formulaire pour choisir le gagnant du Prix.
    """
    def __init__(self, list_choices=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if list_choices:
            self.winner.choices = list_choices

    winner = SelectField("Gagnant", choices=[])
    submit = SubmitField("Confirmer")

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class InputForm(FlaskForm):

    input_one = StringField('Ticker: ', validators = [DataRequired()])
    submit = SubmitField('Search')

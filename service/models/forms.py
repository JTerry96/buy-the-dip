from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class InputForm(FlaskForm):

    input_one = StringField('Ticker: ', validators = [DataRequired()])
    submit = SubmitField('Search')

class FilterForm(FlaskForm):

    ath_low = StringField('ATH Low: ', validators = [DataRequired()])
    ath_high = StringField('ATH High: ', validators = [DataRequired()])
    submit = SubmitField('Filter')

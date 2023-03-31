from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class InputForm(FlaskForm):

    input_one = StringField('First input: ', validators = [DataRequired()])
    input_two = StringField('Second input: ', validators = [DataRequired()])
    submit = SubmitField('Search')

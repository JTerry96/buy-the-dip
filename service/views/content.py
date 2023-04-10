from flask import Blueprint, render_template
from service import db
from service.models.model import Relationships
from service.models.forms import InputForm
from pytrends.request import TrendReq

relationship_blueprint = Blueprint('relationship',__name__, template_folder='templates')


@relationship_blueprint.route('/find_relation', methods = ['GET', 'POST'])
def find_relation():

    input_one = 'Butterflies'
    input_two = 'Bitcoin'

    form = InputForm()

    if form.validate_on_submit():

        input_one = form.input_one.data
        input_two = form.input_two.data
    
        new_relation = Relationships(input_one, input_two)

    pytrend = TrendReq(hl='en-US', tz=360)

    kw_list = [input_one, input_two]

    pytrend.build_payload([kw_list[0]], timeframe='today 12-m', geo='', gprop='')
    df = pytrend.interest_over_time()

    pytrend.build_payload([kw_list[1]], timeframe='today 12-m', geo='', gprop='')
    df1 = pytrend.interest_over_time()

    correlation = "{:.5f}".format(df[kw_list[0]].corr(df1[kw_list[1]]))

    dates = list(df.index)
    labels = []
    for i in dates:
        labels.append(str(i))

    values_a = list(df[kw_list[0]])
    values_b = list(df1[kw_list[1]])

    if form.validate_on_submit():

        new_relation.correlation = correlation
        db.session.add(new_relation)
        db.session.commit()
    
    return render_template("find_relation.html", form = form, labels=labels, values_a=values_a, values_b=values_b, kw_list = kw_list, correlation=correlation)


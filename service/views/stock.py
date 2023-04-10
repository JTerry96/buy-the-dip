from flask import Blueprint, render_template
from service import db
from service.models.forms import InputForm

from service.application_service import get_stock_service


stock_blueprint = Blueprint(
    'stock',
    __name__,
    template_folder='templates'
)


@stock_blueprint.route('/get-stock-price', methods = ['GET', 'POST'])
def get_stock_price():
    """Get stock price"""
    form = InputForm()

    if form.validate_on_submit():

        ticker = form.input_one.data
        period = form.input_two.data

        stock = get_stock_service(ticker=ticker, period=period)
        data = stock.display_last_low()

        print (data)
    
    return render_template("stock.html", form=form)


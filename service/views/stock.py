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
    stock = get_stock_service()
    data = stock.get_data()

    if form.validate_on_submit():
        ticker = form.input_one.data
        period = form.input_two.data

        stock.add_ticker(ticker=ticker, period=period)

        data = stock.get_data()
    return render_template("stock.html", form=form, data=data)


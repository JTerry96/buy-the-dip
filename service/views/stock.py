from flask import Blueprint, render_template, flash
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
    data = stock.get_all()

    if form.validate_on_submit():
        try:
            ticker = form.input_one.data.upper()
            stock.add_ticker(ticker=ticker)
            data = stock.get_all()

        except Exception as error:
            flash(f"Error: {error}", "danger")
            return render_template("stock.html", form=form, data=data)
    return render_template("stock.html", form=form, data=data)


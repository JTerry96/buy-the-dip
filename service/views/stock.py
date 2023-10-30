from flask import Blueprint, render_template, flash, redirect, url_for
from service.models.forms import InputForm
from service.application_service import get_stock_service
import plotly.graph_objs as go
from utilities.data_convert import DictConverter
import ast


stock_blueprint = Blueprint(
    'stock',
    __name__,
    template_folder='templates'
)


@stock_blueprint.route('/get-stock-price', methods=['GET', 'POST'])
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
            flash(f"Added ticker: {ticker} successfully.", "success")

        except Exception as error:
            flash(f"Error: {error}", "danger")
            return render_template("stock.html", form=form, data=data)
    return render_template("stock.html", form=form, data=data)


@stock_blueprint.route('/update', methods=['GET', 'POST'])
def update_tickers():
    """Update tickers."""
    try:
        stock = get_stock_service()
        stock.update_yfinance_ticker_data()

        response_body = {
            "type": "success",
            "status": "success",
            "message": "Successfully updated all tickers."
        }

    except Exception as error:
        error_message = str(error)
        response_body = {
            "type": "danger",
            "status": "error",
            "message": error_message,
            "text": error_message
        }

    flash(response_body["message"], response_body["type"])
    return redirect(url_for("stock.get_stock_price"))


@stock_blueprint.route('/view-ticker-data/<string:ticker>', methods=['GET', 'POST'])
def view_ticker_data(ticker):
    """View ticker data"""
    stock = get_stock_service()
    data = stock._stock_repo.get_by_ticker(ticker=ticker)

    historic_data = DictConverter.dict_to_list(list_dict=ast.literal_eval(data.historic_data))

    graph_bulk_speed = go.Figure(
        data=[
            go.Scatter(
                x=historic_data['DateTimeString'],
                y=historic_data['Close'],
                mode="markers",
            )
        ],
        layout=go.Layout(title="Price vs Time"),
    )
    stuff=graph_bulk_speed.to_json()

    return render_template(
        "individual_stock.html",
        graph_bulk_speed=stuff
    )

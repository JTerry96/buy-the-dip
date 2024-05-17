from flask import Blueprint, render_template, flash, redirect, url_for, request
from service.models.forms import InputForm, FilterForm
from service.application_service import get_stock_service
import plotly.graph_objs as go
from utilities.data_convert import DictConverter
import ast
from utilities.data_convert import YfCsvReader
from service.exceptions import ServiceException


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


@stock_blueprint.route(
    '/view-ticker-data/<string:ticker>',
    methods=['GET', 'POST']
)
def view_ticker_data(ticker):
    """View ticker data"""
    stock = get_stock_service()
    data = stock._stock_repo.get_by_ticker(ticker=ticker)

    historic_data = DictConverter.dict_to_list(
        list_dict=ast.literal_eval(
            data.historic_data
        )
    )

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
    stuff = graph_bulk_speed.to_json()

    return render_template(
        "individual_stock.html",
        graph_bulk_speed=stuff
    )


@stock_blueprint.route('/stock-screener', methods=['GET', 'POST'])
def stock_screener():
    """Screen stocks."""
    form = FilterForm()
    stock = get_stock_service()
    data = stock.get_all()

    if form.validate_on_submit():
        low = form.ath_low.data
        high = form.ath_high.data
        try:
            data = stock.get_by_all_time_high(
                low=low,
                high=high
            )
            flash(
                f"Now displaying all stocks with a current ATH (All Time High)"
                f" percentage from {low}% to {high}%.", "success")

        except Exception as error:
            flash(f"Error: {error}", "danger")
            return render_template("filter.html", form=form, data=data)
    return render_template("filter.html", form=form, data=data)


@stock_blueprint.route('/bulk-add-csv', methods=['GET', 'POST'])
def bulk_add_csv():
    """Bulk adds the ticker data from a yfinance csv file to the db."""
    stock = get_stock_service()
    if request.method == 'POST':
        csv_file = request.files['csv_file']
        symbols = YfCsvReader.extract_symbols(csv_file=csv_file)
        if symbols:
            for symbol in symbols:
                try:
                    ticker = symbol.upper()
                    stock.add_ticker(ticker=ticker)
                    flash(f"Added ticker: {symbol} successfully.", "success")

                except ServiceException as error:
                    flash(f"Error: {error}", "danger")

        else:
            flash("Error: No symbols found in CSV file.", "danger")

    return render_template("bulk_add_csv.html")

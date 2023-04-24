"""Stock price application service"""
import yfinance as yahooFinance
from datetime import datetime, timedelta
from service.schemas.stock import Stock
from service.repos import Stock as StockRepo
from service.exceptions import ServiceException
from service.models.stock import Stock as StockModel

class StockPrice():
    """Application service to retrieve stock price"""
    def __init__(
        self,
        stock_repo: StockRepo
    ):
        """Initialize stock price service"""
        self._stock_repo = stock_repo

    def add_ticker(self, ticker: str) -> None:
        """Add ticker to database"""
        stock = self._analyse_data(ticker=ticker)

        if stock_model:=self._check_exists(ticker=ticker):
            self._stock_repo.update(stock_model)
        else:
            self._stock_repo.add(stock)

        self._stock_repo.commit()

    def _analyse_data(self, ticker: str) -> Stock:
        """Analyse stock price data and return a dataset including the last
        low date.

        Returns:
            Stock: Stock Model
        """
        data = self._get_price(ticker=ticker)
        data['DateTime'] = data.index

        data = data.to_dict('records')

        time_since = datetime.now() - timedelta(days=365)
        last_low_price = 0
        current_price = data[-1]['Close']

        for point in data[0:int(len(data)*0.9)]:
            if self._is_between(
                current_price,
                point['Close'],
                last_low_price
            ):
                time_since = data[-1]['DateTime']-point['DateTime']
                last_low = point['DateTime']
                last_low_price = point['Close']
        
        return Stock(
            ticker=ticker,
            current_price=round(
                number=current_price,
                ndigits=2
            ),
            time_since=time_since,
            last_low=last_low,
        )

    def _get_price(self, ticker: str):
        """Retrieve stock price from Yahoo Finance"""
        data = yahooFinance.Ticker(
            ticker=ticker
        )

        data = data.history(period=StockModel.PERIOD)
        if len(data) == 0:
            raise ServiceException(
                "Could not retrieve data from Yahoo Finance."
            )
        return data

    def _is_between(
        self,
        value,
        first_range_value,
        second_range_value
    ):
        """Check if value is between one and two"""
        upper_bound = max(first_range_value, second_range_value)
        lower_bound = min(first_range_value, second_range_value)
        return lower_bound <= value <= upper_bound

    def get_all(self):
        """Get stock price info from database"""
        stocks = self._stock_repo.get_all()

        return [
            {
                'ticker': stock.ticker,
                'current_price': stock.current_price,
                'time_since': stock.time_since,
                'last_low': stock.last_low,
            } for stock in stocks
        ]

    def _check_exists(self, ticker: str):
        """Check if ticker exists in database"""
        return self._stock_repo.get_by_ticker(ticker=ticker)

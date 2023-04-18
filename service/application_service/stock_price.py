"""Stock price application service"""
import yfinance as yahooFinance
from datetime import datetime, timedelta
from service.schemas.stock import Stock
from service.repos import get_stock_repo, Stock as StockRepo

class StockPrice():
    """Application service to retrieve stock price"""
    def __init__(
        self,
        stock_repo: StockRepo
    ):
        """Initialize stock price service"""
        self._stock_repo = stock_repo

    def add_ticker(self, ticker: str, period: str) -> None:
        """Add ticker to database"""
        stock = self._analyse_data(ticker=ticker, period=period)
        self._stock_repo.add(stock)
        self._stock_repo.commit()

    def _analyse_data(self, ticker: str, period: str,) -> Stock:
        """Analyse stock price data and return a dataset including the last
        low date.

        Returns:
        """
        data = self._get_price(ticker=ticker, period=period)
        data['DateTime'] = data.index

        data = data.to_dict('records')

        last_low_date = datetime.now() - timedelta(days=365)
        last_low_price = 0
        current_price = data[-1]['Close']

        for point in data[0:int(len(data)*0.9)]:
            if self._is_between(
                current_price,
                point['Close'],
                last_low_price
            ):
                last_low_date = point['DateTime']
                last_low_price = point['Close']
        
        return Stock(
            ticker=ticker,
            current_price=current_price,
            last_low=last_low_date
        )

    def _get_price(self, ticker: str, period: str,):
        """Retrieve stock price from Yahoo Finance"""
        data = yahooFinance.Ticker(
            ticker=ticker
        )
        return data.history(period=period)

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

    def get_data(self):
        """Get stock price info from database"""
        stocks = self._stock_repo.get_all()

        return [
            {
                'ticker': stock.ticker,
                'current_price': stock.current_price,
                'last_low': stock.last_low
            } for stock in stocks
        ]

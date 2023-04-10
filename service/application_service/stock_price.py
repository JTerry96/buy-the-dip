"""Stock price application service"""
import yfinance as yahooFinance
import datetime
from service.models.stock import Stock

class StockPrice():
    """Application service to retrieve stock price"""
    def __init__(self, ticker, period):
        """Initialize stock price service"""
        self._ticker = ticker
        self._period = period

    def display_last_low(self):
        """Display last low"""
        data = self._get_price(ticker=self._ticker, period=self._period)

        last_low = datetime.datetime.now() - self._period
        for point in data:
            if point['Open'] <= last_low:
                last_low = point['Open']
        
        stock = Stock(
            ticker=self._ticker,
            current_price=data['Close'],
            last_low=last_low
        )

        return stock

    def _get_price(self):
        """Retrieve stock price from Yahoo Finance"""
        data = yahooFinance.Ticker(
            self._ticker
        )
        return data.history(period=self._period)

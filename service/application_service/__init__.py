"""Application service module"""
from service.application_service.stock_price import StockPrice


def get_stock_service(ticker, period):
    """Get stock price service"""
    return StockPrice(
        ticker=ticker,
        period=period
    )

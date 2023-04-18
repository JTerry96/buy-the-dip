"""Application service module"""
from service.application_service.stock_price import StockPrice
from service.repos import get_stock_repo


def get_stock_service():
    """Get stock price service"""
    return StockPrice(
        stock_repo=get_stock_repo()
    )

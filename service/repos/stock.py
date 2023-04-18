""""""
from service.models.stock import Stock as StockModel
from service.schemas.stock import Stock as StockSchema
from service.repos.base import BaseRepository

class Stock(BaseRepository):

    _model = StockModel
    _schema = StockSchema

    def get_by_ticker(self, ticker):
        """Get a stock by ticker"""
        return self._schema.query.filter_by(ticker=ticker).first()
    
    def get_all(self):
        """Get all stocks"""
        return self._schema.query.all()


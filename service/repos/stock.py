""""""
from service.models.stock import Stock as StockModel
from service.schemas.stock import Stock as StockSchema
from service.repos.base import BaseRepository

class Stock(BaseRepository):

    _model = StockModel
    _schema = StockSchema

    def get_by_ticker(self, ticker) -> StockSchema:
        """Get a stock by ticker"""
        return self._schema.query.filter_by(ticker=ticker).first()
    
    def get_by_all_time_high(self, low:float, high:float) -> StockSchema:
        """Gets a selection of data filtering by All Time High."""
        return self._schema.query.filter(
            self._schema.percentage_of_ath>=low,
            self._schema.percentage_of_ath<=high
            ).all(
        )

    def get_all(self):
        """Get all stocks"""
        return self._schema.query.order_by(self._schema.ticker.asc()).all()
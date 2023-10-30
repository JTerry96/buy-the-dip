"""Stock Model"""
from service import db

class Stock(db.Model):

    __tablename__ = 'stock'

    id = db.Column(db.Integer,primary_key=True)
    ticker = db.Column(db.String(50))
    current_price = db.Column(db.Float)
    last_low = db.Column(db.Date)
    time_since = db.Column(db.Interval)
    percentage_of_ath = db.Column(db.Float)
    historic_data = db.Column(db.String)

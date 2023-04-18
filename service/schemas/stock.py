"""Stock Model"""
from service import db

class Stock(db.Model):

    __tablename__ = 'stock'

    id = db.Column(db.Integer,primary_key=True)
    ticker = db.Column(db.String(50))
    current_price = db.Column(db.Float)
    last_low = db.Column(db.Date)
    

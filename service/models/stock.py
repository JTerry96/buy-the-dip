""""""
from service import db

class Stock(db.Model):

    __tablename__ = 'stock'

    id = db.Column(db.Integer,primary_key=True)
    ticker = db.Column(db.Text)
    current_price = db.Column(db.Float)
    last_low = db.Column(db.Integer)


db.create_all()
db.session.commit()

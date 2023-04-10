"""Stock model"""
from sqlalchemy import Column, Integer, Boolean
import datetime

class Stock():
    """Stock model"""
    id: int
    ticker: str
    current_price: float
    last_low: datetime.date

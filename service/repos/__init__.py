"""This module contains the repositories for the application."""
from .stock import Stock
from service import db

def get_stock_repo(db=db) -> Stock:
    """Get the stock repository"""
    return Stock(db=db)

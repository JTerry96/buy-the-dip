

class StockPrice():
    """Application service to retrieve stock price"""
    def get_price(ticker, start_date, end_date):
        """Retrieve stock price from Yahoo Finance"""
        df = web.DataReader(ticker, 'yahoo', start_date, end_date)
        return df['Adj Close']

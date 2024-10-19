from typing import Dict
from api.api_client import APIClient
from enum import Enum
    
class Interval(Enum):
    """ 
    Enumeration for time intervals used in stock data retrieval
    
    Values:
        ONE_MIN: 1 minute interval
        FIVE_MIN: 5 minute interval
        FIFTEEN_MIN: 15 minute interval
        THIRTY_MIN: 30 minute interval
        SIXTY_MIN: 60 minute interval
    """
    
    ONE_MIN = '1min'
    FIVE_MIN = '5min'
    FIFTEEN_MIN = '15min'
    THIRTY_MIN = '30min'
    SIXTY_MIN = '60min'

class FinanceAPI(APIClient):
    """
    API client for accessing financial data from Alpha Vantage.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(FinanceAPI, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, api_key: str):
        """
        Initializes the AlphaVantageAPI client with the provided API key.

        :param api_key: Alpha Vantage API key.
        """
        if not hasattr(self, 'initialized'):  # Ensure __init__ is only called once
            super().__init__('https://www.alphavantage.co')
            self.api_key = api_key
            self.initialized = True

    def authenticate(self):
        """
        Alpha Vantage uses API keys passed as query parameters.
        No additional authentication steps are required.
        """
        pass  # Authentication handled via API key in parameters

    def get_stock_intraday(self, symbol: str, interval: Interval) -> Dict[str, any]:
        """
        Retrieves stock data for the specified symbol.

        :param symbol: Stock symbol (e.g., "AAPL").
        :param interval: Interval for the time series (e.g., Interval.ONE_MIN, Interval.FIVE_MIN).
        :return: Stock data as a dictionary.
        """
        params = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': symbol,
            'interval': interval.value,
            'apikey': self.api_key
        }
        return self.get('query', params=params)
    
    def get_stock_daily(self, symbol: str, compact: bool = True) -> Dict[str, any]:
        """
        Retrieves daily stock data for the specified symbol.

        :param symbol: Stock symbol (e.g., "AAPL").
        :param compact: Whether to use compact representation (default is True).
        :return: Stock data as a dictionary.
        """
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'outputsize': 'compact' if compact else 'full',
            'apikey': self.api_key
        }
        return self.get('query', params=params)
    
    def get_stock_latest(self, symbol: str) -> Dict[str, any]:
        """
        Retrieves the latest stock data for the specified symbol.

        :param symbol: Stock symbol (e.g., "AAPL").
        :return: Stock data as a dictionary.
        """
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol,
            'apikey': self.api_key
        }
        return self.get('query', params=params)
    
    def search_symbols(self, keywords: str) -> Dict[str, any]:
        """
        Searches for stock symbols based on the specified keywords.

        :param keywords: Keywords to search for.
        :return: Search results as a dictionary.
        """
        params = {
            'function': 'SYMBOL_SEARCH',
            'keywords': keywords,
            'apikey': self.api_key
        }
        return self.get('query', params=params)
    
    def get_market_status(self) -> Dict[str, any]:
        """
        Retrieves the current market status.

        :return: Market status as a dictionary.
        """
        params = {
            'function': 'MARKET_STATUS',
            'apikey': self.api_key
        }
        return self.get('query', params=params)
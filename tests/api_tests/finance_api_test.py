import unittest
from unittest.mock import patch, MagicMock
from api.finance_api import FinanceAPI, Interval

class TestFinanceAPI(unittest.TestCase):

    def setUp(self):
        self.api_key = 'test_api'
        self.finance_api = FinanceAPI(self.api_key)
        self.url = 'https://www.alphavantage.co'

    def test_initialization(self):
        self.assertEqual(self.finance_api.api_key, self.api_key)
        self.assertEqual(self.finance_api.base_url, 'https://www.alphavantage.co')

    @patch('requests.get')
    def test_get_stock_intraday(self, mock_get):
        mock_response = MagicMock()
        expected_data = {'Time Series (1min)': {'2021-01-01 09:30:00': {'1. open': '150.00'}}}
        mock_response.json.return_value = expected_data
        mock_get.return_value = mock_response

        stock_data = self.finance_api.get_stock_intraday('AAPL', Interval.ONE_MIN)
        self.assertEqual(stock_data, expected_data)
        mock_get.assert_called_once_with(
            self.url + '/query',
            headers={},
            params={
                'function': 'TIME_SERIES_INTRADAY',
                'symbol': 'AAPL',
                'interval': '1min',
                'apikey': self.api_key
            }
        )

    @patch('requests.get')
    def test_get_stock_daily(self, mock_get):
        mock_response = MagicMock()
        expected_data = {'Time Series (Daily)': {'2021-01-01': {'1. open': '150.00'}}}
        mock_response.json.return_value = expected_data
        mock_get.return_value = mock_response

        stock_data = self.finance_api.get_stock_daily('AAPL')
        self.assertEqual(stock_data, expected_data)
        mock_get.assert_called_once_with(
            self.url + '/query',
            headers={},
            params={
                'function': 'TIME_SERIES_DAILY',
                'symbol': 'AAPL',
                'outputsize': 'compact',
                'apikey': self.api_key
            }
        )

    @patch('requests.get')
    def test_get_stock_latest(self, mock_get):
        mock_response = MagicMock()
        expected_data = {'Global Quote': {'01. symbol': 'AAPL', '05. price': '150.00'}}
        mock_response.json.return_value = expected_data
        mock_get.return_value = mock_response

        stock_data = self.finance_api.get_stock_latest('AAPL')
        self.assertEqual(stock_data, expected_data)
        mock_get.assert_called_once_with(
            self.url + '/query',
            headers={},
            params={
                'function': 'GLOBAL_QUOTE',
                'symbol': 'AAPL',
                'apikey': self.api_key
            }
        )

    @patch('requests.get')
    def test_search_symbols(self, mock_get):
        mock_response = MagicMock()
        expected_data = {'bestMatches': [{'1. symbol': 'AAPL', '2. name': 'Apple Inc.'}]}
        mock_response.json.return_value = expected_data
        mock_get.return_value = mock_response

        search_results = self.finance_api.search_symbols('Apple')
        self.assertEqual(search_results, expected_data)
        mock_get.assert_called_once_with(
            self.url + '/query',
            headers={},
            params={
                'function': 'SYMBOL_SEARCH',
                'keywords': 'Apple',
                'apikey': self.api_key
            }
        )

    @patch('requests.get')
    def test_get_market_status(self, mock_get):
        mock_response = MagicMock()
        expected_data = {'marketStatus': 'open'}
        mock_response.json.return_value = expected_data
        mock_get.return_value = mock_response

        market_status = self.finance_api.get_market_status()
        self.assertEqual(market_status, expected_data)
        mock_get.assert_called_once_with(
            self.url + '/query',
            headers={},
            params={
                'function': 'MARKET_STATUS',
                'apikey': self.api_key
            }
        )
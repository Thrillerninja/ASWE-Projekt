import unittest
from unittest.mock import patch, MagicMock
from usecases.financetracker_state import FinanceState
from usecases.state_machine import StateMachine
import json

class TestFinanceState(unittest.TestCase):

    @patch('usecases.financetracker_state.FinanceState.get_information')
    @patch('usecases.financetracker_state.APIFactory.create_api')
    def test_on_enter(self, mock_create_api, mock_get_information):
        # Set up the state machine and the finance state
        state_machine = StateMachine()
        financetracker_state = FinanceState(state_machine)

        # Mock APIs
        mock_tts_api = MagicMock()
        mock_stock_api = MagicMock()
        mock_create_api.side_effect = [mock_tts_api, mock_stock_api]

        # Simulate the data returned from the stock API
        stock_data = {
            "most_actively_traded": [
                {"ticker": "AAPL", "price": "150", "change_amount": "2", "change_percentage": "1.35%", "volume": "3000000"},
                {"ticker": "GOOGL", "price": "2800", "change_amount": "10", "change_percentage": "0.36%", "volume": "2500000"},
                {"ticker": "TSLA", "price": "700", "change_amount": "5", "change_percentage": "0.72%", "volume": "2200000"}
            ]
        }

        # Mock the stock API's get_top_gainers_losers function
        mock_stock_api.get_top_gainers_losers.return_value = stock_data

        # Mock get_information method to return a valid name for each stock
        mock_get_information.side_effect = ["Apple", "Google", "Tesla"]

        # Call on_enter method
        financetracker_state.on_enter()

        # Check if the TTS API was called with the expected output
        mock_tts_api.speak.assert_any_call("Die drei Meistgehandelten Aktien heute sind Apple, Google und Tesla.")
        mock_tts_api.speak.assert_any_call("Hier ist dein tägliches Update für die Apple-Aktie. Der aktuelle Kurs liegt bei 150.0 Dollar. Heute hat sich der Kurs um 2.0 Dollar geändert, was eine Änderung von 1.4 Prozent bedeutet. Das Handelsvolumen liegt bei 3.0 Mio. gehandelten Aktien.")
        mock_tts_api.speak.assert_any_call("Hier ist dein tägliches Update für die Google-Aktie. Der aktuelle Kurs liegt bei 2800.0 Dollar. Heute hat sich der Kurs um 10.0 Dollar geändert, was eine Änderung von 0.4 Prozent bedeutet. Das Handelsvolumen liegt bei 2.5 Mio. gehandelten Aktien.")
        mock_tts_api.speak.assert_any_call("Hier ist dein tägliches Update für die Tesla-Aktie. Der aktuelle Kurs liegt bei 700.0 Dollar. Heute hat sich der Kurs um 5.0 Dollar geändert, was eine Änderung von 0.7 Prozent bedeutet. Das Handelsvolumen liegt bei 2.2 Mio. gehandelten Aktien.")

    @patch('usecases.financetracker_state.APIFactory.create_api')
    def test_round_numbers_for_speech(self, mock_create_api):
        state_machine = StateMachine()
        financetracker_state = FinanceState(state_machine)

        # Mock APIs
        mock_tts_api = MagicMock()
        mock_stock_api = MagicMock()
        mock_create_api.side_effect = [mock_tts_api, mock_stock_api]

        # Sample data to test the rounding function
        raw_data = [
            {"name": "Stock1", "price": "123.4567", "change_amount": "12.345", "change_percentage": "1.23%", "volume": "1000000000"},
            {"name": "Stock2", "price": "789.1234", "change_amount": "9.876", "change_percentage": "0.98%", "volume": "500000"}
        ]
        
        # Call round_numbers_for_speech
        rounded_data = financetracker_state.round_numbers_for_speech(raw_data)

        # Check if the rounding works correctly
        self.assertEqual(rounded_data[0]["price"], 123.46)
        self.assertEqual(rounded_data[0]["change_amount"], 12.35)
        self.assertEqual(rounded_data[0]["change_percentage"], 1.2)
        self.assertEqual(rounded_data[0]["volume"], "1.0 Mrd.")
        
        self.assertEqual(rounded_data[1]["price"], 789.12)
        self.assertEqual(rounded_data[1]["change_amount"], 9.88)
        self.assertEqual(rounded_data[1]["change_percentage"], 1.0)
        self.assertEqual(rounded_data[1]["volume"], "500.0 Tsd.")

    @patch('usecases.financetracker_state.APIFactory.create_api')
    def test_get_information(self, mock_create_api):
        state_machine = StateMachine()
        financetracker_state = FinanceState(state_machine)

        # Mock APIs
        mock_tts_api = MagicMock()
        mock_stock_api = MagicMock()
        mock_create_api.side_effect = [mock_tts_api, mock_stock_api]

        # Mock the stock API's company_overview method
        mock_stock_api.company_overview.return_value = {"Name": "Apple Inc."}

        # Test the get_information method
        result = financetracker_state.get_information("AAPL")
        self.assertEqual(result, "Apple Inc.")

    @patch('usecases.financetracker_state.APIFactory.create_api')
    def test_on_enter_with_api_limit(self, mock_create_api):
        state_machine = StateMachine()
        financetracker_state = FinanceState(state_machine)

        # Mock APIs
        mock_tts_api = MagicMock()
        mock_stock_api = MagicMock()
        mock_create_api.side_effect = [mock_tts_api, mock_stock_api]

        # Simulate API rate limit response
        mock_stock_api.get_top_gainers_losers.return_value = {
            "Information": "Thank you for using Alpha Vantage! Our standard API rate limit is 25 requests per day. Please subscribe to any of the premium plans at https://www.alphavantage.co/premium/ to instantly remove all daily rate limits."
        }

        # Mock file loading behavior
        mock_file = MagicMock()
        mock_file.__enter__.return_value = mock_file
        mock_file.read.return_value = '{"most_actively_traded": [{"ticker": "AAPL", "price": "150", "change_amount": "2", "change_percentage": "1.35%", "volume": "3000000"}]}'
        
        # Simulate the data reading when API is limited
        with patch("builtins.open", return_value=mock_file):
            financetracker_state.on_enter()

        # Check if the file was used
        mock_file.read.assert_called()

if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch, MagicMock, mock_open, Mock
from usecases.financetracker_state import FinanceState
from usecases.state_machine import StateMachine
import json

class TestFinanceState(unittest.TestCase):


    def setUp(self):
        self.mock_state_machine = MagicMock(spec=StateMachine)
        self.mock_api_factory = MagicMock()
        self.mock_state_machine.api_factory = self.mock_api_factory
        self.mock_state_machine.exit_finance = MagicMock()
        self.finance_state = FinanceState(self.mock_state_machine)

    # Simulate the data returned from the stock API
    #stock_data = {
    #    "most_actively_traded": [
    #        {"ticker": "AAPL", "price": "150", "change_amount": "2", "change_percentage": "1.35%", "volume": "3000000"},
    #        {"ticker": "GOOGL", "price": "2800", "change_amount": "10", "change_percentage": "0.36%", "volume": "2500000"},
    #        {"ticker": "TSLA", "price": "700", "change_amount": "5", "change_percentage": "0.72%", "volume": "2200000"}
    #    ]
    #}

#%%%%%%%%%%%%%%%%%%%%%tests für round_numbers_for_speech%%%%%%%%%%%%%%%%%%%
    def test_rounding_and_formatting(self):
        input_data = [
            {
                "name": "Stock A",
                "price": "123.456",
                "change_amount": "1.2345",
                "change_percentage": "3.5678%",
                "volume": 1500
            },
            {
                "name": "Stock B",
                "price": "987.654",
                "change_amount": "-2.3456",
                "change_percentage": "-1.2345%",
                "volume": 2_000_000
            },
            {
                "name": "Stock C",
                "price": "50.5",
                "change_amount": "0",
                "change_percentage": "0%",
                "volume": 500
            }
        ]
        expected_output = [
            {
                "name": "Stock A",
                "price": 123.46,
                "change_amount": 1.23,
                "change_percentage": 3.6,
                "volume": "1.5 Tsd."
            },
            {
                "name": "Stock B",
                "price": 987.65,
                "change_amount": -2.35,
                "change_percentage": -1.2,
                "volume": "2.0 Mio."
            },
            {
                "name": "Stock C",
                "price": 50.5,
                "change_amount": 0.0,
                "change_percentage": 0.0,
                "volume": "500"
            }
        ]
        self.assertEqual(self.finance_state.round_numbers_for_speech(input_data), expected_output)

    def test_empty_input(self):
        input_data = []
        expected_output = []
        self.assertEqual(self.finance_state.round_numbers_for_speech(input_data), expected_output)

    def test_large_volume(self):
        input_data = [
            {
                "name": "Stock D",
                "price": "1.0",
                "change_amount": "0.0",
                "change_percentage": "0%",
                "volume": 3_000_000_000
            }
        ]
        expected_output = [
            {
                "name": "Stock D",
                "price": 1.0,
                "change_amount": 0.0,
                "change_percentage": 0.0,
                "volume": "3.0 Mrd."
            }
        ]
        self.assertEqual(self.finance_state.round_numbers_for_speech(input_data), expected_output)

    def test_small_values(self):
        input_data = [
            {
                "name": "Stock E",
                "price": "0.12345",
                "change_amount": "0.00123",
                "change_percentage": "0.01234%",
                "volume": 999
            }
        ]
        expected_output = [
            {
                "name": "Stock E",
                "price": 0.12,
                "change_amount": 0.0,
                "change_percentage": 0.0,
                "volume": "999"
            }
        ]
        self.assertEqual(self.finance_state.round_numbers_for_speech(input_data), expected_output)

#%%%%%%%%%%%%%%%%%%%%%tests für get_information%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def test_rate_limit_reached(self):
        # Simuliert die Rückgabe der Rate-Limit-Nachricht
        self.finance_state.stock_api.company_overview.return_value = {
            "Information": "Thank you for using Alpha Vantage! Our standard API rate limit is 25 requests per day. Please subscribe to any of the premium plans at https://www.alphavantage.co/premium/ to instantly remove all daily rate limits."
        }
        result = self.finance_state.get_information("AAPL")
        self.assertEqual(result, {})

    def test_no_data_returned(self):
        # Simuliert den Fall, in dem keine Daten zurückgegeben werden
        self.finance_state.stock_api.company_overview.return_value = {}
        result = self.finance_state.get_information("AAPL")
        self.assertEqual(result, "AAPL")

    def test_valid_data_returned(self):
        # Simuliert den Fall, in dem gültige Daten zurückgegeben werden
        self.finance_state.stock_api.company_overview.return_value = {"Name": "Apple Inc.", "Symbol": "AAPL"}
        result = self.finance_state.get_information("AAPL")
        self.assertEqual(result, "Apple Inc.")

#%%%%%%%%%%%%%%%%%%%%%tests für on_enter%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.join", return_value="temp.json")
    @patch("json.dump")
    @patch.object(FinanceState, "get_information")  # Mock der get_information Methode
    #@patch.object(FinanceState, "stock_api")  # Mock für die stock_api
    def test_on_enter_valid_data(self, mock_get_information, mock_json_dump, mock_path_join, mock_open_file):
        # Simuliert die Antwort der API
        self.finance_state.stock_api = Mock()

        self.finance_state.stock_api.get_top_gainers_losers.return_value = {
            "most_actively_traded": [
                {"ticker": "AAPL"}, {"ticker": "MSFT"}, {"ticker": "GOOG"}
            ]
        }

        # Simuliert die Rückgabe von get_information für die Ticker
        def mock_get_info_side_effect(symbol):
            if symbol == "AAPL":
                return "Apple Inc."
            elif symbol == "MSFT":
                return "Microsoft Corp."
            elif symbol == "GOOG":
                return "Google LLC"
            return symbol  # Fallback, falls kein Ticker erkannt wird

        # Setzen des Mocks für get_information
        mock_get_information.side_effect = mock_get_info_side_effect

        print(type(mock_get_information))
        # Mock für round_numbers_for_speech, um die erwarteten gerundeten Daten zurückzugeben
        mock_round_numbers = MagicMock(return_value=[
            {"name": "Apple Inc.", "price": 150, "change_amount": 2, "change_percentage": "1.5", "volume": "10 Mio."},
            {"name": "Microsoft Corp.", "price": 250, "change_amount": -1, "change_percentage": "-0.4", "volume": "12 Mio."},
            {"name": "Google LLC", "price": 2800, "change_amount": 15, "change_percentage": "0.5", "volume": "8 Mio."}
        ])

        # Setzen des Mocks für round_numbers_for_speech
        self.finance_state.round_numbers_for_speech = mock_round_numbers
        # Führe die Methode on_enter aus
        self.finance_state.on_enter()

        # Überprüfen, ob get_information für die drei Ticker aufgerufen wurde
        mock_get_information.assert_any_call("AAPL")
        mock_get_information.assert_any_call("MSFT")
        mock_get_information.assert_any_call("GOOG")
        
        # Überprüfen, ob die tts_api die korrekte Nachricht spricht
        self.finance_state.tts_api.speak.assert_any_call("Die drei Meistgehandelten Aktien heute sind Apple Inc., Microsoft Corp. und Google LLC.")
        self.finance_state.tts_api.speak.assert_any_call(
            "Hier ist dein tägliches Update für die Apple Inc.-Aktie. Der aktuelle Kurs liegt bei 150 Dollar. Heute hat sich der Kurs um 2 Dollar geändert, was eine Änderung von 1.5 Prozent bedeutet. Das Handelsvolumen liegt bei 10 Mio. gehandelten Aktien.")
        self.finance_state.tts_api.speak.assert_any_call(
            "Hier ist dein tägliches Update für die Microsoft Corp.-Aktie. Der aktuelle Kurs liegt bei 250 Dollar. Heute hat sich der Kurs um -1 Dollar geändert, was eine Änderung von -0.4 Prozent bedeutet. Das Handelsvolumen liegt bei 12 Mio. gehandelten Aktien.")
        self.finance_state.tts_api.speak.assert_any_call(
            "Hier ist dein tägliches Update für die Google LLC-Aktie. Der aktuelle Kurs liegt bei 2800 Dollar. Heute hat sich der Kurs um 15 Dollar geändert, was eine Änderung von 0.5 Prozent bedeutet. Das Handelsvolumen liegt bei 8 Mio. gehandelten Aktien.")

        # Überprüfen, ob json.dump einmal aufgerufen wurde
        mock_json_dump.assert_called_once()

        # Überprüfen, ob exit_finance aufgerufen wurde
        self.finance_state.state_machine.exit_finance.assert_called_once()


    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([
            {"name": "Apple Inc.", "price": 150, "change_amount": 2, "change_percentage": "1.5%", "volume": 10000000},
            {"name": "Microsoft Corp.", "price": 250, "change_amount": -1, "change_percentage": "-0.4%", "volume": 12000000},
            {"name": "Google LLC", "price": 2800, "change_amount": 15, "change_percentage": "0.5%", "volume": 8000000}
        ]))
    @patch("os.path.join", return_value="temp.json")
    def test_on_enter_no_data(self, mock_path_join, mock_open_file):
        # Simuliert keine Daten von der API
        self.finance_state.stock_api.get_top_gainers_losers.return_value = {}

        self.finance_state.on_enter()

        # Prüfen, ob Fallback-Daten geladen wurden
        mock_open_file.assert_any_call("temp.json", "r")
        self.finance_state.tts_api.speak.assert_any_call("Die drei Meistgehandelten Aktien heute sind Apple Inc., Microsoft Corp. und Google LLC.")


    
    
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([
            {"name": "Apple Inc.", "price": 150, "change_amount": 2, "change_percentage": "1.5%", "volume": 10000000},
            {"name": "Microsoft Corp.", "price": 250, "change_amount": -1, "change_percentage": "-0.4%", "volume": 12000000},
            {"name": "Google LLC", "price": 2800, "change_amount": 15, "change_percentage": "0.5%", "volume": 8000000}
        ]))
    @patch("os.path.join", return_value="temp.json")
    @patch("json.dump")
    def test_on_enter_rate_limit(self, mock_json_dump, mock_path_join, mock_open_file):
        # Simuliert Rate-Limit-Meldung von der API
        self.finance_state.stock_api.get_top_gainers_losers.return_value = {
            "Information": "Thank you for using Alpha Vantage! Our standard API rate limit is 25 requests per day. Please subscribe to any of the premium plans at https://www.alphavantage.co/premium/ to instantly remove all daily rate limits."
        }

        self.finance_state.on_enter()

        # Überprüfen, ob Fallback-Daten geladen wurden
        mock_open_file.assert_any_call("temp.json", "r")
        self.finance_state.tts_api.speak.assert_any_call("Die drei Meistgehandelten Aktien heute sind Apple Inc., Microsoft Corp. und Google LLC.")
        mock_json_dump.assert_called_once()


if __name__ == '__main__':
    unittest.main()

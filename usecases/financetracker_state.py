
from api.api_factory import APIFactory
from typing import Dict
import json
import os
class FinanceState:
    """
    State that represents the finance tracker state/usecase of the application.
    """
    
    def __init__(self, state_machine):
        self.state_machine = state_machine
        
        self.tts_api = self.state_machine.api_factory.create_api(api_type="tts")
        self.stock_api = self.state_machine.api_factory.create_api(api_type="finance")

        print("FinanceTrackerState initialized")

    def on_enter(self):
        """
        Function executed when the state is entered.
        It outputs the top 3 most traded stocks.
        """
        print("FinanceTrackerState entered")
        
        data = self.stock_api.get_top_gainers_losers()
        if data == {} or data == {"Information": "Thank you for using Alpha Vantage! Our standard API rate limit is 25 requests per day. Please subscribe to any of the premium plans at https://www.alphavantage.co/premium/ to instantly remove all daily rate limits."}:
            file_path = os.path.join(os.getcwd(), "ASWE-Projekt", "usecases", "temp.json")
            with open(file_path, "r") as file:
                data = json.load(file)
        else:
            top_three_actively_traded = data["most_actively_traded"][:3]
            data = []
            for stock in top_three_actively_traded:
                name = self.get_information(stock["ticker"])
                if name == {}:
                    stock["name"] = name
                    del stock["ticker"]
                    data.append(stock)
                else:
                    file_path = os.path.join(os.getcwd(), "ASWE-Projekt", "usecases", "temp.json")
                    with open(file_path, "r") as file:
                        data = json.load(file)
        
        print(f"Die drei Meistgehandelten Aktien heute sind {data[0]["name"]}, {data[1]["name"]} und {data[2]["name"]}.")
        for stock in data:
            print(f"Hier ist dein tägliches Update für die {stock["name"]}-Aktie. Der aktuelle Kurs liegt bei {stock["price"]} Dollar. Heute ist der Kurs um {stock["change_amount"]} Dollar gestiegen, was eine Änderung von {stock["change_percentage"]} Prozent bedeutet. Das Handelsvolumen liegt bei {stock["volume"]} gehandelten Aktien.")
        
        self.state_machine.exit_finance()

    def get_information(self, symbol):
        data = self.stock_api.company_overview(symbol)
        if data == {"Information": "Thank you for using Alpha Vantage! Our standard API rate limit is 25 requests per day. Please subscribe to any of the premium plans at https://www.alphavantage.co/premium/ to instantly remove all daily rate limits."}:
            return {}
        else:
            name = data["Name"]
            return name
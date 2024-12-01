
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


    def round_numbers_for_speech(self, data):
        """
        Rounds the data of the finance API so it sounds better when outputtet by tts
        """
        def format_volume(volume):
            volume = int(volume)
            if volume >= 1_000_000_000:
                return f"{round(volume / 1_000_000_000, 1)} Mrd."
            elif volume >= 1_000_000:
                return f"{round(volume / 1_000_000, 1)} Mio."
            elif volume >= 1_000:
                return f"{round(volume / 1_000, 1)} Tsd."
            else:
                return str(volume)

        rounded_data = []
        for item in data:
            rounded_item = {
                "name": item["name"],
                "price": round(float(item["price"]), 2),
                "change_amount": round(float(item["change_amount"]), 2),
                "change_percentage": round(float(item["change_percentage"].strip('%')), 1),
                "volume": format_volume(item["volume"])
            }
            rounded_data.append(rounded_item)
        return rounded_data

    def on_enter(self):
        """
        Function executed when the state is entered.
        It outputs the top 3 most traded stocks.
        """
        print("FinanceTrackerState entered")
        
        file_path = os.path.join(os.getcwd(), "ASWE-Projekt", "usecases", "temp.json")
        data = self.stock_api.get_top_gainers_losers()
        if data == {} or data == {"Information": "Thank you for using Alpha Vantage! Our standard API rate limit is 25 requests per day. Please subscribe to any of the premium plans at https://www.alphavantage.co/premium/ to instantly remove all daily rate limits."}:
            with open(file_path, "r") as file:
                data = json.load(file)
                print("laden1")
        else:
            top_three_actively_traded = data["most_actively_traded"][:3]
            data = []
            print(top_three_actively_traded)
            for stock in top_three_actively_traded:
                name = self.get_information(stock["ticker"])
                if name != {}:
                    stock["name"] = name
                    del stock["ticker"]
                    data.append(stock)
                else:
                    with open(file_path, "r") as file:
                        data = json.load(file)
                        print("laden2")
        
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
            print("data dumped")

        data = self.round_numbers_for_speech(data)

        self.tts_api.speak(f"Die drei Meistgehandelten Aktien heute sind {data[0]['name']}, {data[1]['name']} und {data[2]['name']}.")
        for stock in data:
            self.tts_api.speak(f"Hier ist dein tägliches Update für die {stock['name']}-Aktie. Der aktuelle Kurs liegt bei {stock['price']} Dollar. Heute hat sich der Kurs um {stock['change_amount']} Dollar geändert, was eine Änderung von {stock['change_percentage']} Prozent bedeutet. Das Handelsvolumen liegt bei {stock["volume"]} gehandelten Aktien.")
        
        self.state_machine.exit_finance()

    def get_information(self, symbol):
        data = self.stock_api.company_overview(symbol)
        if data == {"Information": "Thank you for using Alpha Vantage! Our standard API rate limit is 25 requests per day. Please subscribe to any of the premium plans at https://www.alphavantage.co/premium/ to instantly remove all daily rate limits."}:
            return {}
        elif data == {}:
            return symbol
        else:

            print("Daten für den ticker:\n",data)
            name = data["Name"]
            return name
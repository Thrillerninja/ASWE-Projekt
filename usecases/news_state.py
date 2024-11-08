from api.news_api.main import NewsAPI

class NewsState:
    """
    State that represents the news state/use case of the application.
    """

    def __init__(self, state_machine):
        self.state_machine = state_machine
        self.tts_api = self.state_machine.api_factory.create_api(api_type="tts")
        self.news_api = NewsAPI()  # Use the custom NewsAPI class
        
        print("NewsState initialized")

    def on_enter(self):
        """
        Function executed when the state is entered.
        It retrieves and provides the user with the latest news.
        """
        print("NewsState entered")
        
        # Retrieve the latest headlines from the NewsAPI client
        headlines = self.news_api.get_headlines()

        if headlines:
            # Read out the first few headlines
            for headline in headlines[:3]:  # Limiting to the first 3 headlines
                self.tts_api.speak(f"Headline: {headline}")
            
            self.tts_api.speak("Wollen sie die Zusammenfassung eines Artikels hören?")
            self.state_machine.news_interact()


        else:
            # If no news is available, inform the user and return to interaction state
            self.tts_api.speak("Es tut mir leid, es sind keine Nachrichten verfügbar.")
            self.state_machine.news_idle()  # Transition to interaction state

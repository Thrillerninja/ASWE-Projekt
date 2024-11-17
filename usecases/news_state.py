from api.news_api.main import NewsAPI
import datetime
from loguru import logger

class NewsState:
    """
    State that represents the news state/use case of the application.
    """

    def __init__(self, state_machine):
        """
        Initializes the NewsState object.

        Args:
            state_machine: The state machine object.
        """
        self.state_machine = state_machine
        self.tts_api = self.state_machine.api_factory.create_api(api_type="tts")
        self.news_api = NewsAPI()  # Use the custom NewsAPI class

        logger.add(
            "news_state.log", rotation="500 MB", level="DEBUG"
        )  # Add file logging
        logger.info("NewsState initialized")

    def on_enter(self):
        """
        Function executed when the state is entered.
        It retrieves and provides the user with the latest news.
        """
        logger.info("NewsState entered")

        # Retrieve the latest headlines from the NewsAPI client
        headlines = self.news_api.get_headlines()

        if headlines:
            # Read out the first few headlines
            for headline in headlines[:5]:  # Limiting to the first 3 headlines
                self.tts_api.speak(f"Headline: {headline}")
                logger.debug(f"Read headline: {headline}")

            self.tts_api.speak("Wollen sie die Zusammenfassung eines Artikels hören?")
            start_time = datetime.datetime.now().timestamp()
            while (
                self.running and datetime.datetime.now().timestamp() - start_time < 10
            ):
                self.check_userinput()
            self.running = False
            self.voice_interface.play_sound("idle")
            self.voice_interface.speak("Spracherkennung beendet.")
            logger.debug("Speech recognition ended.")

        else:
            # If no news is available, inform the user and return to interaction state
            self.tts_api.speak("Es tut mir leid, es sind keine Nachrichten verfügbar.")
            self.state_machine.news_idle()  # Transition to interaction state

    def check_userinput(self):
        """
        Listens for user input and determines the next action.
        """
        user_input = self.tts_api.listen()
        if not user_input:
            self.tts_api.speak("Keine Eingabe erkannt. Bitte versuchen Sie es erneut.")
            logger.debug("No user input detected.")
            return

        logger.info(f"User said: {user_input}")
        if self.testing:
            self.running = False

        # Interpret the user's input and trigger the appropriate state transition
        if "nein" in user_input.lower() or "exit" in user_input.lower():
            self.tts_api.speak(
                "Du willst nichts weiteres zu einem der Artikel hören. Okay!"
            )
            self.state_machine.news_idle()
            logger.debug("User wants to exit the news state.")
        elif "ja" in user_input.lower() or "yes" in user_input.lower():
            self.tts_api.speak("Welchen Artikel möchten Sie hören?")
            article = self.tts_api.listen()
            self.tts_api.speak("Hier ist die Zusammenfassung des Artikels.")
            summary = self.news_api.get_article_summary(article)
            self.tts_api.speak(summary)
            self.tts_api.speak("Möchten Sie noch eine Zusammenfassung hören?")
            logger.debug("User wants to hear an article summary.")
        elif "nein" in user_input.lower() or "no" in user_input.lower():
            self.tts_api.speak("Spracherkennung beendet.")
            self.state_machine.news_idle()
            logger.debug("User wants to end speech recognition.")
        else:
            self.tts_api.speak(
                "Ich habe Sie nicht verstanden. Bitte wiederholen Sie Ihre Eingabe."
            )
            self.check_userinput()
            logger.debug("User input not understood.")

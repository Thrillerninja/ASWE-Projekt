import datetime
from loguru import logger
import re
from api.news_api.main import NewsAPI
from api.llm_api.llm_api import LLMApi


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
        self.running = True
        self.state_machine = state_machine
        self.llm_api = LLMApi()
        self.tts_api = self.state_machine.api_factory.create_api(api_type="tts", state_machine=self.state_machine)
        self.news_api = self.state_machine.api_factory.create_api(api_type="news")
        logger.info("NewsState initialized")

    def on_enter(self):
        """
        Function executed when the state is entered.
        It retrieves and provides the user with the latest news.
        """
        logger.info("NewsState entered")

        # Retrieve the latest headlines from the NewsAPI client
        headlines = self.news_api.fetch_top_headlines()

        if headlines:
            logger.info("Enter if state for headlines")
            # Read out the first few headlines
            for i, headline in enumerate(headlines[:3]):  # Limiting to the first 3 headlines
                self.tts_api.speak(f"Artikel {i + 1}: {headline["title"]}")
                logger.debug(f"Read headline{i + 1}: {headline}")

            self.tts_api.speak("Wollen sie die Zusammenfassung eines Artikels hören?")
            start_time = datetime.datetime.now().timestamp()
            logger.debug("About to enter while loop")

            # Limit the runtime of the loop to 10 seconds
            while self.running:
                if datetime.datetime.now().timestamp() - start_time >= 10:
                    logger.debug("Time limit exceeded, exiting loop.")
                    break

                result = self.read_article(headlines=headlines)
                if result == "exit":
                    logger.debug("Exiting news state from read_article.")
                    break

            logger.debug("Exiting news state.")
            self.state_machine.news_idle()  # Transition to interaction state

        else:
            logger.info("Enter else state for no headlines")
            # If no news is available, inform the user and return to interaction state
            self.tts_api.speak("Es tut mir leid, es sind keine Nachrichten verfügbar.")
            logger.debug("Exiting news state.")
            self.state_machine.news_idle()  # Transition to interaction state

    def read_article(self, headlines):
        """
        Listens for user input and determines the next action based on the input.

        Args:
            headlines (list): A list of article headlines.

        Returns:
            str: Returns "exit" to signal loop termination.
        """
        logger.debug("Entering read_article method.")
        user_input = self.tts_api.listen()
        logger.debug(f"User input: {user_input}")

        if not user_input:
            self.tts_api.speak("Keine Eingabe erkannt.")
            logger.debug("No user input detected.")
            return "exit"  # Exit loop

        if "nein" in user_input.lower() or "exit" in user_input.lower() or "stop" in user_input.lower():
            self.tts_api.speak("Du willst nichts weiteres zu einem der Artikel hören. Okay!")
            return "exit"  # Exit loop

        self.tts_api.speak("Zu welchem Artikel willst du eine Zusammenfassung hören?")
        user_input = self.tts_api.listen()
        if not user_input:
            self.tts_api.speak("Keine Eingabe erkannt. Bitte versuchen Sie es erneut.")
            logger.debug("No user input detected.")
            return "exit"  # Exit loop
        user_input = user_input.lower()
        try:
            if any([substring in user_input for substring in ["erst", "1", "eins"]]): 
                article_number = 1
            elif any([substring in user_input for substring in ["zwei", "2"]]):
                article_number = 2
            elif any([substring in user_input for substring in ["drei", "3", "dritt"]]):
                article_number = 3
            else:
                logger.error(f"No Number found in LLM Response. Using default 1")
                article_number = 1
                self.tts_api.speak("Ich habe dich nicht ganz verstanden. Ich fasse den ersten Artikel zusammen!")
            # article = self.news_api.get_article(article_number)
            article = headlines[article_number-1]
            content = self.news_api.get_article(article["url"])
            if not content:
                logger.error("Artikel wurde nicht gefunden")
                self.tts_api.speak("Ich konnte den Artikel leider nicht finden")
                return "exit"
            summary = self.news_api.summarize_article(content)
            logger.debug(f"Article summary: {summary}")
            self.tts_api.speak(summary)
            self.tts_api.speak("Ich hoffe der Artikel war interessant für dich.")
            return "exit"
        except Exception as e:
            logger.error(f"Error summarizing article: {e}")
            self.tts_api.speak("Es tut mir leid, ich konnte den Artikel nicht zusammenfassen.")
            return "exit"  # Exit loop

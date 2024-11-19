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
        self.tts_api = self.state_machine.api_factory.create_api(api_type="tts")
        self.news_api = NewsAPI()   
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
            for headline in headlines[:3]:  # Limiting to the first 3 headlines
                self.tts_api.speak(f"Headline: {headline}")
                logger.debug(f"Read headline: {headline}")

            self.tts_api.speak("Wollen sie die Zusammenfassung eines Artikels hören?")
            start_time = datetime.datetime.now().timestamp()
            while (
                self.running and datetime.datetime.now().timestamp() - start_time < 10
            ):
                self.read_article(headlines=headlines)
            logger.debug("Exeting news state.")
            self.state_machine.news_idle()  # Transition to interaction state

        else:
            # If no news is available, inform the user and return to interaction state
            self.tts_api.speak("Es tut mir leid, es sind keine Nachrichten verfügbar.")
            logger.debug("Exeting news state.")
            self.state_machine.news_idle()  # Transition to interaction state

    def read_article(self, headlines):
        """
        Listens for user input and determines the next action based on the input.

        Args:
            headlines (list): A list of article headlines.

        Behavior:
            - Listens for user input using the TTS API.
            - If no input is detected, prompts the user to try again and retries the process.
            - If the input contains "nein", "exit", or "stop", transitions to the news idle state.
            - Otherwise, asks the user which article they want a summary of.
            - Listens for the user's choice of article.
            - If no input is detected, prompts the user to try again and retries the process.
            - Uses the LLM API to determine which headline the user is interested in.
            - Summarizes the selected article using the News API and speaks the summary.
            - Handles exceptions during the summarization process and transitions to the news idle state if an error occurs.
        """
        user_input = self.tts_api.listen()
        if not user_input:
            self.tts_api.speak("Keine Eingabe erkannt. Bitte versuchen Sie es erneut.")
            logger.debug("No user input detected.")
            self.read_article(headlines=headlines) # try again
        elif "nein" in user_input.lower() or "exit" in user_input.lower() or "stop" in user_input.lower():
            self.tts_api.speak("Du willst nichts weiteres zu einem der Artikel hören. Okay!")
            self.state_machine.news_idle()
        else:
            self.tts_api.speak("Zu welchem Artikel willst du eine Zusammenfassung hören?")
            user_input = self.tts_api.listen()
            if not user_input:
                self.tts_api.speak("Keine Eingabe erkannt. Bitte versuchen Sie es erneut.")
                logger.debug("No user input detected.")
                self.read_article(headlines=headlines)
            else:
                message = f"This is input from a user: {user_input}. These are possible headlines: {headlines}. Which headline interests the user the most?. Respond with the number of headlien the user is interested in."
                response = self.llm_api.get_response(model="llama3.2:1b", message_content=message)
                logger.debug(f"LLM response: {response}")
                article_number = int(re.search(r'\d+', response).group())  
                logger.debug(f"User is interested in article number {article_number}")
                try:
                    article= self.news_api.get_article(article_number)
                    summary = self.news_api.summarize_article(article)
                except Exception as e:
                    logger.error(f"Error summarizing article: {e}")
                    self.tts_api.speak("Es tut mir leid, ich konnte den Artikel nicht zusammenfassen.")
                    self.state_machine.news_idle()
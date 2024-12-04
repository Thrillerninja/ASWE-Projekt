
import os
from dotenv import load_dotenv
from loguru import logger
from newsapi.newsapi_client import NewsApiClient
from api.llm_api import LLMApi


class NewsAPI():
    """
    API client for accessing news articles using NewsAPI and summarizing them with an LLM model.

    Attributes:
        _instance (NewsAPI): Singleton instance of the NewsAPI class.
        client (NewsApiClient): The client to interact with the NewsAPI service.
        date (str): The date for filtering news articles (not currently used).
        headlines (list): List of top news headlines retrieved from the NewsAPI.
        llmclient (LLMApi): The LLM client for summarizing articles.
    """
    _instance = None
    client = None
    date = None
    headlines = None
    llmclient = LLMApi()

    def __new__(cls, *args, **kwargs):
        """
        Ensures that only one instance of the NewsAPI client is created (Singleton pattern).

        Returns:
            NewsAPI: The singleton instance of the NewsAPI class.
        """
        if cls._instance is None:
            cls._instance = super(NewsAPI, cls).__new__(cls)
            load_dotenv()  # Load environment variables from the .env file
        return cls._instance

    def __init__(self) -> None:
        """
        Initializes the NewsAPI client, retrieves the API key from environment variables,
        and fetches the top headlines.

        Raises:
            ValueError: If the API key is not found in the .env file.
        """
        # Load environment variables
        load_dotenv()
        
        # Retrieve the API key from environment variable
        api_key = os.getenv('NEWS_API_KEY')
        
        # Check if API key is provided
        if not api_key:
            raise ValueError("API key not found. Please check your .env file.")
        
        # Initialize the NewsAPI client with the retrieved API key
        self.client = NewsApiClient(api_key=api_key)
        
        # Log that the instance was successfully initialized
        logger.info("NewsAPI instance initialized.")
        
        # Fetch the top headlines immediately upon instantiation
        self.headlines = self.fetch_top_headlines()

    def fetch_top_headlines(self):
        """
        Fetches the top headlines from the NewsAPI service.

        Returns:
            list: A list of top headlines (titles) from the fetched articles.
        """
        headlines = self.client.get_top_headlines(language='en', country='us')
        
        # Extract and return the titles of the articles from the response
        return [article['title'] for article in headlines['articles']]
    
    def get_headlines(self):
        """
        Returns the list of top headlines that were fetched during initialization.

        Returns:
            list: The list of headlines retrieved from the NewsAPI service.
        """
        return self.headlines
    
    def get_article(self, headline_index: int):
        """
        Retrieves the full content of an article based on its index in the headlines list.

        Args:
            headline_index (int): The index of the headline in the list.

        Returns:
            list: A list of article contents corresponding to the selected headline.
        """
        # Fetch the article content based on the headline
        content = self.client.get_everything(q=self.headlines[headline_index])
        
        # Extract and return the content of the articles
        return [article['content'] for article in content['articles']]

    def summarize_article(self, content: str):
        """
        Uses the LLM client to summarize a given article content.

        Args:
            content (str): The content of the article to be summarized.

        Returns:
            str: The summarized version of the provided article content.
        """
        # Send the content to the LLM model to summarize the article
        return self.llmclient.get_response(
            model="llama3.2:1b",
            message_content=f"Schreibe einen kurzen Text (1-4 Sätze) über diese Überschrift auf Deutsch. Verwende keine Sonderzeichen: {content}"
        )

import os
from dotenv import load_dotenv
from loguru import logger
from newsapi.newsapi_client import NewsApiClient
from api.llm_api import LLMApi
import html
import requests
import json


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
        
        self.articles = None
        self.source = 'die-zeit,focus,bild'

    @property
    def amount_articles(self):
        return len(self.articles)

    def fetch_top_headlines(self):
        '''return and refresh the articles with the top headlines'''
        response = self.client.get_top_headlines(language='de', sources=self.source)
        if response['status'] == 'ok':
            self.articles = response['articles']
            for article in self.articles:
                article['title'] = html.unescape(article['title'])
        return self.articles
    
    
#    def get_headlines(self):
#        """
#        Returns the list of top headlines that were fetched during initialization.
#
#        Returns:
#            list: The list of headlines retrieved from the NewsAPI service.
#        """
#        return self.headlines
    
    def get_article(self, url: str):
        article_response = requests.get(url)
        if article_response.status_code != 200:
            print(f"Failed to retrieve article. Status code: {article_response.status_code}")
            return
        # print(article_response.text)
        for line in article_response.text.split('\n'):
            linestart = "\"articleBody\": "
            if line.strip().startswith(linestart):
                line = line.strip(linestart).split("©")[0]  # ignore dpa and other sources in string
                return html.unescape(line)  # &#34; -> "
        return


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
            message_content=f"Fasse diesn Artikel in 1-4 Sätzen auf deutsch zusammen. Verwende keine Sonderzeichen:\n{content}"
        )
import requests
import os
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker

class ActionAskAboutWorld(Action):

    def name(self) -> str:
        return "action_ask_about_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        # Get the latest news from an API (NewsAPI in this example)
        api_key = os.getenv('ca6b11a4337043e88e6912aa4dcc9209')
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
        response = requests.get(url)
        news_data = response.json()

        # Extract the title of the latest news article
        if news_data.get("articles"):
            latest_news = news_data["articles"][0]["title"]
        else:
            latest_news = "Sorry, I couldn't fetch the latest news."

        # Return the latest news in the response
        dispatcher.utter_message(text=f"The latest news is: {latest_news}")

        return []

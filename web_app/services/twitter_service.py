# web_app/services/twitter_service.py

import os
from types import SimpleNamespace
from dotenv import load_dotenv
from requests_oauthlib import OAuth1Session

load_dotenv()

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

BASE_URL = "https://api.twitter.com/1.1"


class TwitterClient:
    """The two Twitter v1.1 calls this app uses (replaces tweepy, which pins a vulnerable oauthlib)."""

    def __init__(self):
        self.session = OAuth1Session(TWITTER_API_KEY, TWITTER_API_SECRET,
                                     TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

    def _get(self, path, **params):
        response = self.session.get(f"{BASE_URL}/{path}", params=params)
        response.raise_for_status()
        # attribute access (user.screen_name, status.full_text), like tweepy models
        return response.json(object_hook=lambda d: SimpleNamespace(**d))

    def get_user(self, screen_name):
        return self._get("users/show.json", screen_name=screen_name)

    def user_timeline(self, screen_name, **params):
        return self._get("statuses/user_timeline.json", screen_name=screen_name, **params)


def twitter_api_client():
    return TwitterClient()


if __name__ == "__main__":

    api = twitter_api_client()
    user = api.get_user("elonmusk")
    print("USER", user)
    print(user.screen_name)
    print(user.name)
    print(user.followers_count)

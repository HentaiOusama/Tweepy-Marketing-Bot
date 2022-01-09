import webbrowser

import tweepy


class TwitterAPI:
    def __init__(self, consumer_key, consumer_key_secret, callback_uri="oob"):
        self.consumerKey = consumer_key
        self.consumerKeySecret = consumer_key_secret
        self.callback_uri = callback_uri
        self.auth: tweepy.OAuthHandler | None = None
        self.api: tweepy.API | None = None
        self.hasAuthorizedUser = False

    def authorize_new_user(self, should_print_access_credentials=False):
        self.auth = tweepy.OAuthHandler(consumer_key=self.consumerKey, consumer_secret=self.consumerKeySecret,
                                        callback=self.callback_uri)
        redirect_url = self.auth.get_authorization_url()
        webbrowser.open(redirect_url)
        user_account_pin = input("Enter the pin : ")

        self.auth.get_access_token(user_account_pin)
        if should_print_access_credentials:
            print(f"Access Token : {self.auth.access_token}")
            print(f"Access Token Secret : {self.auth.access_token_secret}")
        self.api = tweepy.API(self.auth)

    def authorize_existing_user(self, access_key, access_key_secret):
        self.auth = tweepy.OAuthHandler(consumer_key=self.consumerKey, consumer_secret=self.consumerKeySecret)
        self.auth.set_access_token(access_key, access_key_secret)
        self.api = tweepy.API(self.auth)

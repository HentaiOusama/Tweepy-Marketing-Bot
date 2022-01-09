import tweepy


class TwitterClient:
    def __init__(self, consumer_key, consumer_key_secret, bearer_token, access_key, access_secret_key):
        self.client: tweepy.Client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_key_secret,
            bearer_token=bearer_token,
            access_token=access_key,
            access_token_secret=access_secret_key
        )

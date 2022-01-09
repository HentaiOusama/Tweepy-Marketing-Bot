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

    def get_user_id(self, username: str) -> int:
        user = self.client.get_user(username=username)
        return user.data.id

    def get_user_followers(self, user_id: int | None = None, username: str = "") -> [tweepy.User]:
        if user_id is None:
            user_id = self.get_user_id(username)
        response = self.client.get_users_followers(id=user_id, max_results=1000)
        return response.data

    def like_and_retweet(self, tweet_id: int | str, should_like, should_retweet=False,
                         should_quote_tweet=False, quote_text=""):
        if should_like:
            self.client.like(tweet_id)
        if should_retweet:
            self.client.retweet(tweet_id)
        if should_quote_tweet:
            self.client.create_tweet(quote_tweet_id=tweet_id, text=quote_text)

    def undo_like_and_retweet(self, tweet_id: int | str, should_unlike, should_unretweet=False):
        if should_unlike:
            self.client.unlike(tweet_id)
        if should_unretweet:
            self.client.unretweet(tweet_id)

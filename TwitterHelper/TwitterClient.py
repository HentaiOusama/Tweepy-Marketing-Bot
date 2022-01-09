import tweepy

from Interface.UserData import UserData
from MongoDB.DBHandler import DBHandler


class TwitterClient:
    def __init__(self, consumer_key, consumer_key_secret, bearer_token, access_key,
                 access_secret_key, db_handler: DBHandler):
        self.db_handler = db_handler
        self.client: tweepy.Client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_key_secret,
            bearer_token=bearer_token,
            access_token=access_key,
            access_token_secret=access_secret_key
        )

    def get_user_details(self, user_id: int | None = None, username: str | None = None, search_db=True) -> UserData:
        user = self.db_handler.get_user(user_id, username)
        if search_db and (user is not None):
            return user
        else:
            if user_id is not None:
                user = self.client.get_user(id=user_id, user_fields=["public_metrics"])
            else:
                user = self.client.get_user(username=username, user_fields=["public_metrics"])

            user = UserData(user.data.id, user.data.username, user.data.public_metrics["followers_count"],
                            user.data.public_metrics["following_count"])
            self.db_handler.store_user_info(user)
            return user

    def get_user_followers(self, user_id: int | None = None, username: str | None = None,
                           max_results: int = 1000, pagination_token=None, should_store=True):
        if user_id is None:
            user_id = self.get_user_details(username=username).userId
        if pagination_token is None:
            response = self.client.get_users_followers(id=user_id, max_results=max_results,
                                                       user_fields=["public_metrics"])
        else:
            response = self.client.get_users_followers(id=user_id, max_results=max_results,
                                                       user_fields=["public_metrics"],
                                                       pagination_token=pagination_token)

        user_list = []
        for user in response.data:
            current_user = UserData(user.id, user.username, user.public_metrics["followers_count"],
                                    user.public_metrics["following_count"])
            user_list.append(current_user)
            if should_store:
                self.db_handler.store_user_info(current_user)

        return user_list, response.meta.get("previous_token"), response.meta.get("next_token")

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

    def follow_user(self, user_id: int | None = None, username: str | None = None, threshold: int | None = None):
        if threshold is not None:
            user_data = self.get_user_details(user_id=user_id, username=username)
            user_id = user_data.userId
            if user_data.followersCount > threshold:
                return False

        if user_id is None:
            user_id = self.get_user_details(user_id=user_id, username=username).userId

        self.client.follow_user(target_user_id=user_id)
        # TODO : Store the user id in database for future reference
        return True

    def unfollow_user(self, user_id):
        self.client.unfollow_user(target_user_id=user_id)

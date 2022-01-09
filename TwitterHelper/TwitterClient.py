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

    def get_user_followers(self, user_id: int | None = None, username: str = "", max_count: int = 1000,
                           pagination_token=None):
        if user_id is None:
            user_id = self.get_user_id(username)

        if pagination_token is None:
            response = self.client.get_users_followers(id=user_id, max_results=1000, max_count=max_count)
        else:
            response = self.client.get_users_followers(id=user_id, max_results=1000, max_count=max_count,
                                                       pagination_token=pagination_token)

        return response.data, response.meta.get("previous_token"), response.meta.get("next_token")

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

    def follow_user(self, user_id: int, threshold: int | None = None):
        if threshold is not None:
            followers, prev_token, next_token = self.get_user_followers(user_id)
            follow_len = len(followers)
            while next_token is not None:
                followers, prev_token, next_token = self.get_user_followers(user_id, pagination_token=next_token)
                follow_len += len(followers)
                if follow_len > threshold:
                    break

            if follow_len > threshold:
                return False

        self.client.follow_user(target_user_id=user_id)
        # TODO : Store the user id in database for future reference
        return True

    def unfollow_user(self, user_id):
        self.client.unfollow_user(target_user_id=user_id)

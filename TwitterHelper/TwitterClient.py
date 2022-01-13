import sys
import time

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
        self.shouldFetchFollowers = True
        self.shouldFollowUsers = True

    def set_should_fetch_followers(self, value: bool) -> None:
        self.shouldFetchFollowers = value

    def set_should_follow_users(self, value: bool) -> None:
        self.shouldFollowUsers = value

    def get_user_details_from_twitter(self, user_id: int | None = None, username: str | None = None,
                                      search_db: bool = True) -> UserData:
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
            self.db_handler.store_user_info(user, ["userId", "username", "followersCount", "followingCount"])
            return user

    def get_user_followers_from_twitter(self, user_id: int | None = None, username: str | None = None,
                                        max_results: int = 1000, pagination_token: str | None = None,
                                        should_store: bool = False) -> tuple[list[UserData], str, str]:
        if user_id is None:
            user_id = self.get_user_details_from_twitter(username=username).userId

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
                                    user.public_metrics["following_count"], user_id)
            if should_store:
                self.db_handler.store_user_info(current_user, ["userId", "username", "followersCount",
                                                               "followingCount"])
            user_list.append(current_user)

        return user_list, response.meta.get("previous_token", ""), response.meta.get("next_token", "")

    def get_follower_and_store(self, user_id: int, pagination_token: str | None = None, max_results: int = 1000) -> str:
        user_list, previous_token, next_token = \
            self.get_user_followers_from_twitter(user_id=user_id, max_results=max_results,
                                                 pagination_token=pagination_token, should_store=True)
        self.db_handler.store_follow_account_info(user_id, previous_token, next_token)
        return next_token

    def start_fetching_followers(self, user_id: int, max_results: int = 1000,
                                 max_iteration: int | None = None):
        if not self.shouldFetchFollowers:
            return
        print(f"Follower Fetch Request for {user_id}")
        account_info = self.db_handler.get_follow_account_info(user_id=user_id)
        next_token = account_info.get("nextToken") if account_info is not None else None
        if next_token == "":
            next_token = None
        i = 0
        while max_iteration is None or i < max_iteration:
            if not self.shouldFetchFollowers or next_token is None or next_token == "":
                break
            next_token = self.get_follower_and_store(user_id=user_id, max_results=max_results,
                                                     pagination_token=next_token)
            print(f"Received List of Followers : {i}")
            i += 1
            time.sleep(66)  # Keep it 66 seconds to maintain 15 / 15 min request limit.

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

    def follow_user(self, user_id: int | None = None, username: str | None = None):
        if user_id is None:
            user_id = self.get_user_details_from_twitter(user_id=user_id, username=username).userId
        self.client.follow_user(target_user_id=user_id)
        return True

    def start_following_users(self, max_iteration: int | None = None, min_followers: int = 0,
                              max_followers: int = sys.maxsize, min_following: int = 0, end_time: float = 0):
        if not self.shouldFollowUsers:
            return
        elif end_time == 0:
            end_time = time.time() + (23 * 60 * 60)
        find_doc = {
            "didFollow": {"$in": [None, False]},
            "followersCount": {
                "$lte": max_followers,
                "$gte": min_followers
            },
            "followingCount": {
                "$gte": min_following
            }
        }

        user_list = self.db_handler.get_user_from_find_doc(find_doc)
        i = 0
        for user in user_list:
            if (time.time() >= end_time) or (not self.shouldFollowUsers):
                return
            user["didFollow"] = True
            user["areFollowing"] = True
            user["followTime"] = time.time()
            user = UserData.initialize_from_object(user)
            if self.follow_user(user_id=user.userId):
                self.db_handler.store_user_info(user, ["didFollow", "areFollowing", "followTime"])
                i += 1
            if max_iteration is not None and i >= max_iteration:
                break
            time.sleep(20)  # Keep it 20 to maintain 50 / 15 min request limit

        if i == 0:
            print("No users to follow...")
            time.sleep(70)

    def unfollow_user(self, user_id):
        # TODO : Update database
        self.client.unfollow_user(target_user_id=user_id)

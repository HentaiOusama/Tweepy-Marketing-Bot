import os
import sys
import threading
import time

from MongoDB.DBHandler import DBHandler
from TwitterHelper.TwitterAPI import TwitterAPI
from TwitterHelper.TwitterClient import TwitterClient


def get_mongo_keys():
    return str(os.environ.get("mongo_username")), str(os.environ.get("mongo_password")), \
           str(os.environ.get("mongo_cluster_name")), str(os.environ.get("mongo_database_name"))


def get_twitter_keys():
    # Returns Consumer_API_Key, Consumer_API_Secret_Key, Bearer_Token,
    # Access_Token and Access_Token_Secret (Must be set as environment variables).
    return str(os.environ.get("consumer_key")), str(os.environ.get("consumer_key_secret")), \
           str(os.environ.get("bearer_token")), str(os.environ.get("user_access_key")), \
           str(os.environ.get("user_access_secret"))


def initialize_client():
    mun, mps, mcn, mdn = get_mongo_keys()
    db_handler = DBHandler(mun, mps, mcn, mdn)
    ck, cks, bt, ak, aks = get_twitter_keys()
    if (ak == "None") or (aks == "None"):
        t_api = TwitterAPI(consumer_key=ck, consumer_key_secret=cks)
        t_api.authorize_new_user()
        ak, aks = t_api.auth.access_token, t_api.auth.access_token_secret
    t_cli = TwitterClient(consumer_key=ck, consumer_key_secret=cks, bearer_token=bt,
                          access_key=ak, access_secret_key=aks, db_handler=db_handler)
    return t_cli


def continuous_follower():
    end_time = time.time() + (23 * 60 * 60)  # Current Time + 23 hours
    min_followers_count = int(os.environ.get("minFollowersCount", 0))
    max_followers_count = int(os.environ.get("maxFollowersCount", sys.maxsize))
    min_following_count = int(os.environ.get("minFollowingCount", 0))

    print("Starting to follow users from database")
    while time.time() < end_time:
        try:
            tCli.start_following_users(min_followers=min_followers_count, max_followers=max_followers_count,
                                       min_following=min_following_count, end_time=end_time)
        except Exception as err:
            print(err)
    tCli.set_should_fetch_followers(False)
    tCli.set_should_follow_users(False)


def early_use_function():
    user_id = os.environ.get("followUserId", None)
    if user_id is not None:
        user_id = int(user_id)
    else:
        return

    # thread1 = threading.Thread(target=tCli.start_fetching_followers, args=[user_id])
    thread2 = threading.Thread(target=continuous_follower)
    # print("Stating Both Tasks...")
    # thread1.start()
    thread2.start()

    while thread2.is_alive():
        time.sleep(15 * 60)

    # if thread1.is_alive():
    #     thread1.join()
    print("Both Tasks Ended...")


if __name__ == '__main__':
    tCli = initialize_client()

    # Write your code here
    early_use_function()

    print("Waiting 2.5 secs before exit...")
    time.sleep(2.5)
    print("Script Exited")

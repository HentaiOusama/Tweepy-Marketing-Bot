import asyncio
import os
import time

from MongoDB.DBHandler import DBHandler
from TwitterHelper.TwitterAPI import TwitterAPI
from TwitterHelper.TwitterClient import TwitterClient

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


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


def early_use_function():
    end_time = time.time() + (23 * 60 * 60)  # Current Time + 23 hours
    user_id = os.environ.get("followUserId", None)
    if user_id is not None:
        user_id = int(user_id)
    else:
        return
    follow_threshold = os.environ.get("followersThreshold", None)
    if follow_threshold is not None:
        follow_threshold = int(follow_threshold)

    tCli.start_fetching_followers(user_id)
    while time.time() < end_time:
        loop.run_until_complete(tCli.start_following_users(threshold=follow_threshold))


if __name__ == '__main__':
    tCli = initialize_client()

    # Write your code here
    early_use_function()

    print("Waiting 2.5 secs before exit...")
    time.sleep(2.5)
    print("Script Exited")

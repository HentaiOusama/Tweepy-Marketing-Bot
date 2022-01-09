import os
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


def start_fetching_followers(t_client: TwitterClient, user_id: int, max_results: int = 1000):
    account_info = tCli.db_handler.get_follow_account_info(user_id=user_id)
    next_token = account_info.get("nextToken") if account_info is not None else None
    if next_token == "":
        next_token = None
    for i in range(2):
        print(f"Iteration : {i}")
        next_token = tCli.get_follower_and_store(user_id=user_id, max_results=max_results, pagination_token=next_token)
        time.sleep(66)  # Keep it 66 seconds to maintain 15 / 15 min request limit.
        if next_token is None or next_token == "":
            break


if __name__ == '__main__':
    tCli = initialize_client()

    # Write your code here

    print("Waiting 2.5 secs before exit...")
    time.sleep(2.5)
    print("Script Exited")

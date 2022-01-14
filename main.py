import json
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
    min_followers_count = int(os.environ.get("minFollowersCount", 0))
    max_followers_count = int(os.environ.get("maxFollowersCount", sys.maxsize))
    min_following_count = int(os.environ.get("minFollowingCount", 0))

    print("Starting to follow users from database")
    while time.time() < scriptEndTime:
        try:
            tCli.bulk_follow_users(min_followers=min_followers_count, max_followers=max_followers_count,
                                   min_following=min_following_count, end_time=scriptEndTime)
        except Exception as err:
            print(err)


def continuous_tagger():
    found_through_user_id = int(os.environ.get("foundThroughUserId", 0))
    tag_message = str(os.environ.get("baseTagMessage", ""))
    min_followers_count = int(os.environ.get("minFollowersCount", 0))
    max_followers_count = int(os.environ.get("maxFollowersCount", sys.maxsize))
    min_following_count = int(os.environ.get("minFollowingCount", 0))

    print("Starting to tag users from database")
    while time.time() < scriptEndTime:
        try:
            tCli.bulk_tag_users(base_message=tag_message, max_len=270, found_through=found_through_user_id,
                                min_followers=min_followers_count, max_followers=max_followers_count,
                                min_following=min_following_count, end_time=scriptEndTime)
        except Exception as err:
            print(err)


def driver_function():
    run_list = json.loads(str(os.environ.get("threadsToRun", [])))
    threads_to_run = {}

    for key in run_list:
        threads_to_run[key] = True

    thread1 = None
    thread2 = None
    thread3 = None

    if threads_to_run.get("1", False):
        thread1 = threading.Thread(target=continuous_follower)
        thread1.start()
    if threads_to_run.get("2", False):
        user_id = int(os.environ.get("followUserId", 0))
        if user_id != 0:
            thread2 = threading.Thread(target=tCli.start_fetching_followers, args=[user_id], kwargs={
                "end_time": scriptEndTime
            })
            thread2.start()
    if threads_to_run.get("3", False):
        found_through_id = int(os.environ.get("followUserId", 0))
        if found_through_id != 0:
            thread3 = threading.Thread(target=continuous_tagger)
            thread3.start()

    while (thread1 is not None and thread1.is_alive()) or (thread2 is not None and thread2.is_alive()) \
            or (thread3 is not None and thread3.is_alive()):
        time.sleep(15 * 60)

    print("All Tasks Ended...")


if __name__ == '__main__':
    scriptStartTime = time.time()
    scriptEndTime = scriptStartTime + (23 * 60 * 60)
    tCli = initialize_client()

    # Write your code here
    driver_function()

    print("Waiting 2.5 secs before exit...")
    time.sleep(2.5)
    print("Script Exited")

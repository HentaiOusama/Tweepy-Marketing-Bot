import os
import time

from TwitterHelper.TwitterAPI import TwitterAPI
from TwitterHelper.TwitterClient import TwitterClient


def get_keys():
    # Returns Consumer_API_Key, Consumer_API_Secret_Key, Bearer_Token,
    # Access_Token and Access_Token_Secret (Must be set as environment variables).
    return str(os.environ.get("consumer_key")), str(os.environ.get("consumer_key_secret")), \
           str(os.environ.get("bearer_token")), str(os.environ.get("user_access_key")), \
           str(os.environ.get("user_access_secret"))


if __name__ == '__main__':
    ck, cks, bt, ak, aks = get_keys()
    if (ak == "None") or (aks == "None"):
        tAPI = TwitterAPI(consumer_key=ck, consumer_key_secret=cks)
        tAPI.authorize_new_user()
        ak, aks = tAPI.auth.access_token, tAPI.auth.access_token_secret
    tCli = TwitterClient(consumer_key=ck, consumer_key_secret=cks, bearer_token=bt,
                         access_key=ak, access_secret_key=aks)

    # Write your code here

    time.sleep(2.5)
    print("Exiting Program...")

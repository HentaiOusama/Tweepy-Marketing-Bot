import os
import time

import tweepy
import webbrowser


def get_keys():
    # Returns Consumer_API_Key, Consumer_API_Secret_Key, Bearer_Token (Must be set as environment variables.)
    return os.environ.get("consumer_key"), os.environ.get("consumer_key_secret"), os.environ.get("bearer_token")


def authorize_new_user(callback_uri="oob", should_print_access_credentials=False):
    consumer_key, consumer_secret_key, bearer_token = get_keys()
    auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret_key, callback=callback_uri)
    redirect_url = auth.get_authorization_url()
    webbrowser.open(redirect_url)
    user_account_pin = input("Enter the pin : ")

    auth.get_access_token(user_account_pin)
    if should_print_access_credentials:
        print(f"Access Token : {auth.access_token}")
        print(f"Access Token Secret : {auth.access_token_secret}")
    new_api = tweepy.API(auth)
    return new_api, auth.access_token, auth.access_token_secret


def authorize_existing_user(access_key_param, access_key_secret_param):
    consumer_key, consumer_secret_key, bearer_token = get_keys()
    auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret_key)
    auth.set_access_token(access_key_param, access_key_secret_param)
    new_api = tweepy.API(auth)
    return new_api


def getOA2Client(access_key_param, access_secret_key):
    consumer_key, consumer_key_secret, bearer_token = get_keys()
    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_key_secret,
        bearer_token=bearer_token,
        access_token=access_key_param,
        access_token_secret=access_secret_key
    )
    return client


if __name__ == '__main__':
    api, access_key, access_key_secret = authorize_new_user()  # Use once to get access tokens
    api = getOA2Client(access_key, access_key_secret)

    # Write your code here

    time.sleep(2.5)
    print("Exiting Program...")

import copy

import pymongo

from Interface.UserData import UserData


class DBHandler:
    def __init__(self, username: str, password: str, cluster_name: str, database_name: str):
        cluster_name = cluster_name.replace(" ", "").lower()
        connect_url = f"mongodb+srv://{username}:{password}@{cluster_name}.qaot2.mongodb.net/test?retryWrites=true"
        self.cluster = pymongo.MongoClient(connect_url)
        self.database = self.cluster[database_name]

    def get_user(self, user_id: int | None = None, username: str | None = None) -> UserData | None:
        if user_id is not None:
            response = self.database["UserData"].find_one({"userId": user_id})
            return UserData(response["userId"], response["username"],
                            response["followersCount"], response["followingCount"],
                            response["didFollow"], response["areFollowing"],
                            response["followTime"])
        elif username is not None:
            response = self.database["UserData"].find_one({"username": username})
            return UserData(response["userId"], response["username"],
                            response["followersCount"], response["followingCount"],
                            response["didFollow"], response["areFollowing"],
                            response["followTime"])
        else:
            return None

    def store_user_info(self, user_data: UserData, should_remove_optional_data: bool = False):
        find_user_object = {
            "userId": user_data.userId
        }
        data_object = copy.deepcopy(user_data.__dict__)
        if should_remove_optional_data:
            del data_object["didFollow"]
            del data_object["areFollowing"]
            del data_object["followTime"]
        store_user_object = {
            "$set": data_object
        }

        self.database["UserData"].update_one(find_user_object, store_user_object, upsert=True)

    def get_follow_account_info(self, user_id):
        found_document = self.database["FollowAccounts"].find_one({"userId": user_id})
        if found_document:
            return {
                "userId": user_id,
                "nextToken": found_document["nextToken"],
                "previousToken": found_document["previousToken"]
            }
        else:
            return None

    def store_follow_account_info(self, user_id: int, previous_token: str | None = None,
                                  next_token: str | None = None):
        find_document = {
            "userId": user_id
        }
        store_doc = {
            "userId": user_id
        }
        if previous_token is not None and previous_token != "":
            store_doc["previousToken"] = previous_token
        if next_token is not None and next_token != "":
            store_doc["nextToken"] = next_token

        self.database["FollowAccounts"].update_one(find_document, store_doc, upsert=True)

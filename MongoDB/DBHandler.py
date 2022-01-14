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
            return UserData(response["userId"], response["username"], response["followersCount"],
                            response["followingCount"], response.get("foundThrough", 0),
                            response.get("didFollow", False), response.get("areFollowing", False),
                            response.get("followTime", 0), response.get("tagCount", 0))
        elif username is not None:
            response = self.database["UserData"].find_one({"username": username})
            return UserData(response["userId"], response["username"], response["followersCount"],
                            response["followingCount"], response.get("foundThrough", 0),
                            response.get("didFollow", False), response.get("areFollowing", False),
                            response.get("followTime", 0), response.get("tagCount", 0))
        else:
            return None

    def store_user_info(self, user_data: UserData, keys_to_store: list[str] | str = "all"):
        find_user_object = {
            "userId": user_data.userId
        }

        data_object = {}
        if keys_to_store == "all":
            data_object = copy.deepcopy(user_data)
        else:
            for key in keys_to_store:
                data_object[key] = user_data.__dict__[key]

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
        operation_doc = {
            "$set": store_doc
        }

        self.database["FollowAccounts"].update_one(find_document, operation_doc, upsert=True)

    def get_user_from_find_doc(self, find_doc: object):
        return self.database["UserData"].find(find_doc)

import pymongo


class DBHandler:
    def __init__(self, username: str, password: str, cluster_name: str, database_name: str):
        cluster_name = cluster_name.replace(" ", "").lower()
        connect_url = f"mongodb+srv://{username}:{password}@{cluster_name}.zm0r5.mongodb.net/test?retryWrites=true"
        self.cluster = pymongo.MongoClient(connect_url)
        self.database = self.cluster[database_name]

    def get_user(self, user_id: int | None = None, username: str | None = None):
        if user_id is not None:
            return self.database["UserData"].find_one({"userId": user_id})
        elif username is not None:
            return self.database["UserData"].find_one({"username": username})
        else:
            return None

    def store_user_info(self, user_id: int, username: str, follower_count: int, following_count: int):
        find_user_object = {
            "userId": user_id
        }
        store_user_object = {
            "userId": user_id,
            "username": username,
            "followerCount": follower_count,
            "followingCount": following_count
        }

        self.database["UserData"].update_one(find_user_object, store_user_object, upsert=True)

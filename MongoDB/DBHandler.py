import pymongo


class DBHandler:
    def __init__(self, username: str, password: str, cluster_name: str, database_name: str):
        cluster_name = cluster_name.replace(" ", "").lower()
        connect_url = f"mongodb+srv://{username}:{password}@{cluster_name}.zm0r5.mongodb.net/?retryWrites=true"
        self.cluster = pymongo.MongoClient(connect_url)
        self.database = self.cluster[database_name]

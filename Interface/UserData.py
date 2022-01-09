import json


class UserData:
    def __init__(self, user_id: int, username: str, followers_count: int, following_count: int,
                 did_follow: bool, are_following: bool, follow_time: int):
        self.userId: int = user_id
        self.username: str = username
        self.followersCount: int = followers_count
        self.followingCount: int = following_count
        self.didFollow: bool = did_follow
        self.areFollowing: bool = are_following
        self.followTime: int = follow_time

    @staticmethod
    def initialize_from_object(init_object):
        return UserData(init_object["userId"], init_object["username"], init_object["followersCount"],
                        init_object["followingCount"], init_object["didFollow"], init_object["areFollowing"],
                        init_object["followTime"])

    def __repr__(self):
        return json.dumps(self.__dict__)

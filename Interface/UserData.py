import json


class UserData:
    def __init__(self, user_id: int, username: str, followers_count: int, following_count: int,
                 found_through: int = 0, did_follow: bool = False, are_following: bool = False,
                 follow_time: int = 0, did_tag: bool = False):
        self.userId: int = user_id
        self.username: str = username
        self.followersCount: int = followers_count
        self.followingCount: int = following_count
        self.foundThrough: int = found_through
        self.didFollow: bool = did_follow
        self.areFollowing: bool = are_following
        self.followTime: int = follow_time
        self.didTag: bool = did_tag

    @staticmethod
    def initialize_from_object(init_object):
        return UserData(init_object["userId"], init_object["username"], init_object["followersCount"],
                        init_object["followingCount"], init_object.get("foundThrough", 0),
                        init_object.get("didFollow", False), init_object.get("areFollowing", False),
                        init_object.get("followTime", 0), init_object.get("didTag", False))

    def __repr__(self):
        return json.dumps(self.__dict__)

import json


class UserData:
    def __init__(self, user_id: int, username: str, followers_count: int, following_count: int,
                 did_follow: bool, are_following: bool):
        self.userId: int = user_id
        self.username: str = username
        self.followersCount: int = followers_count
        self.followingCount: int = following_count
        self.didFollow: bool = did_follow
        self.areFollowing: bool = are_following

    def __repr__(self):
        return json.dumps(self.__dict__)

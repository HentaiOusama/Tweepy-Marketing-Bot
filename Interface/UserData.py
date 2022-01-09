class UserData:
    def __init__(self, user_id: int, username: str, followers_count: int, following_count: int):
        self.userId: int = user_id
        self.username: str = username
        self.followersCount: int = followers_count
        self.followingCount: int = following_count

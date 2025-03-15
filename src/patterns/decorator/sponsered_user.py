from src.patterns.interfaces.user_decorator import UserDecorator


class SponsoredUser(UserDecorator):
    def __init__(self, user, company_name: str):
        super().__init__(user)
        self.company_name = company_name
        
        # Forward signals from the decorated user
        if hasattr(self._user, 'post_created'):
            self.post_created = self._user.post_created
        if hasattr(self._user, 'follower_added'):
            self.follower_added = self._user.follower_added
        if hasattr(self._user, 'follower_removed'):
            self.follower_removed = self._user.follower_removed

    def get_handle(self) -> str:
        return f"{self._user.handle} [Sponsored]"

    def get_bio(self) -> str:
        return f"Sponsored by {self.company_name}"
        
    # Forward properties to the decorated user
    @property
    def posts(self):
        return self._user.posts
        
    @property
    def followers(self):
        return self._user.followers
        
    # Ensure all user attributes are properly forwarded
    def __getattr__(self, name):
        return getattr(self._user, name)

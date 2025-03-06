from src.interfaces.user_decorator import UserDecorator

class SponsoredUser(UserDecorator):
    """
    Decorator for adding sponsored content to a user's posts.
    implements the UserDecorator interface.

    methods:
    -get_handle : returns the user's handle with [Sponsored] added to the end.
    -get_bio : returns the user's bio with [Sponsored by {company_name}] added to the end.
    """
    def __init__(self, user, company_name: str):
        super().__init__(user)
        self.company_name = company_name

    def get_handle(self) -> str:
        return f"{self._user.handle} [Sponsored]"
    
    def get_bio(self) -> str:
        return f"Sponsored by {self.company_name}"

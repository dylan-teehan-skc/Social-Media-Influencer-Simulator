from src.patterns.interfaces.user_decorator import UserDecorator


class SponsoredUser(UserDecorator):
    def __init__(self, user, company_name: str):
        super().__init__(user)
        self.company_name = company_name

    def get_handle(self) -> str:
        # Use get_handle if available to preserve decorations, otherwise use handle directly
        base_handle = self._user.get_handle() if hasattr(self._user, 'get_handle') else self._user.handle
        return f"{base_handle} [Sponsored]"

    def get_bio(self) -> str:
        return f"Sponsored by {self.company_name}"

    def __getattr__(self, name):
        """Forward all other attributes and methods to the wrapped user."""
        return getattr(self._user, name)

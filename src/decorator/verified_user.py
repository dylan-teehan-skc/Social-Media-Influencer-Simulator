from src.interfaces.user_decorator import UserDecorator


class VerifiedUser(UserDecorator):
    """
    Decorator for adding verified content to a user's posts.
    implements the UserDecorator interface.

    methods:
    -get_handle : returns the user's handle with ✔️ added to the end.
    -get_bio : returns the user's bio with (Verified) added to the end.
    """
    def get_handle(self) -> str:
        return f"{self._user.handle} ✔️"

    def get_bio(self) -> str:
        return f"{self._user.bio} (Verified)"

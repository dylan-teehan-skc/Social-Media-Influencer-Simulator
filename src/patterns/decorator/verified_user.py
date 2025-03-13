from src.patterns.interfaces.user_decorator import UserDecorator


class VerifiedUser(UserDecorator):
    def get_handle(self) -> str:
        return f"{self._user.handle} ✔️"

    def get_bio(self) -> str:
        return f"{self._user.bio} (Verified)"

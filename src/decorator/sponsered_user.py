from src.interfaces.user_decorator import UserDecorator


class SponsoredUser(UserDecorator):
    def __init__(self, user, company_name: str):
        super().__init__(user)
        self.company_name = company_name

    def get_handle(self) -> str:
        return f"{self._user.handle} [Sponsored]"

    def get_bio(self) -> str:
        return f"Sponsored by {self.company_name}"

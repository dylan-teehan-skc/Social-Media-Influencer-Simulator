from src.patterns.interfaces.user_decorator import UserDecorator


class BaseUser(UserDecorator):
    def get_handle(self) -> str:
        return self._user.handle

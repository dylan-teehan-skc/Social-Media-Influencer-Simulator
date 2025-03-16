from src.patterns.interfaces.user_decorator import UserDecorator


class BaseUser(UserDecorator):
    # Base implementation of user decorator that passes through the handle

    def get_handle(self) -> str:
        return self._user.handle

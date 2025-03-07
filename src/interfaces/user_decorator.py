from abc import ABC, abstractmethod


class UserDecorator(ABC):
    """
    Abstract base class for all user decorators.
    Includes the method to get the user's handle.
    """
    def __init__(self, user):
        self._user = user

    @abstractmethod
    def get_handle(self) -> str:
        pass

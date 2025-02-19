from abc import ABC, abstractmethod

class UserDecorator(ABC):
    def __init__(self, user):
        self._user = user

    @abstractmethod
    def get_handle(self) -> str:
        pass
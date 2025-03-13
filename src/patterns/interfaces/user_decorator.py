from abc import ABC, abstractmethod


class UserDecorator(ABC):
    def __init__(self, user):
        self._user = user

    @property
    def handle(self):
        return self.get_handle()

    @property
    def bio(self):
        return self.get_bio()

    @abstractmethod
    def get_handle(self) -> str:
        pass

    @abstractmethod
    def get_bio(self) -> str:
        pass

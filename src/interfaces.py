from abc import ABC, abstractmethod

class GrowthStrategy(ABC):
    @abstractmethod
    def calculate_growth(self, current_value: float, time_period: int) -> float:
        pass

class ContentInterceptor(ABC):
    @abstractmethod
    def intercept(self, post: Post) -> Post:
        pass

class UserDecorator(ABC):
    def __init__(self, user):
        self._user = user

    @abstractmethod
    def get_handle(self) -> str:
        pass

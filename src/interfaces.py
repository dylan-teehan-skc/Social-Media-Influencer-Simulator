from abc import ABC, abstractmethod

class EngagementCommand(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass

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

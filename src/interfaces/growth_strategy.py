from abc import ABC, abstractmethod


class GrowthStrategy(ABC):
    """
    Abstract base class for all growth strategies.
    """
    @abstractmethod
    def calculate_growth(self, current_value: float, time_period: int) -> float:
        pass

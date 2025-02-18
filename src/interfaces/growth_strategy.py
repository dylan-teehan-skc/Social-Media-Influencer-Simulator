from abc import ABC, abstractmethod

class GrowthStrategy(ABC):
    @abstractmethod
    def calculate_growth(self, current_value: float, time_period: int) -> float:
        pass
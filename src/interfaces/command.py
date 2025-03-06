from abc import ABC, abstractmethod

class Command(ABC):
    """
    Abstract base class for all commands.
    """
    @abstractmethod
    def execute(self) -> None:
        pass 
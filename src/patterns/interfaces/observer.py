from abc import ABC, abstractmethod


# pylint: disable=R0903
class Observer(ABC):
    """Interface for observer pattern."""

    @abstractmethod
    def update(self, subject, post=None):
        """Update the observer with new information."""
        pass


class Subject(ABC):
    def __init__(self):
        self._observers = []

    @abstractmethod
    def attach(self, observer: Observer):
        pass

    @abstractmethod
    def detach(self, observer: Observer):
        pass

    @abstractmethod
    def notify(self, post=None):
        pass

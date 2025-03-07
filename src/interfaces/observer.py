from abc import ABC, abstractmethod


# pylint: disable=R0903
class Observer(ABC):
    """
    Abstract base class for all observers.
    Includes the methods to update, attach, detach and notify.
    """
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

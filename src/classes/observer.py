from abc import ABC, abstractmethod

class Observer(ABC):
    """Abstract base class for observers"""
    @abstractmethod
    def update(self, subject, post=None):
        """Method that observers must implement to receive updates"""
        pass

class Subject(ABC):
    """Abstract base class for subjects"""
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        """Attach an observer to the subject"""
        self._observers.append(observer)

    def detach(self, observer: Observer):
        """Detach an observer from the subject"""
        self._observers.remove(observer)

    def notify(self, post=None):
        """Notify all observers about an event"""
        for observer in self._observers:
            observer.update(self, post)
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, subject, post=None):
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
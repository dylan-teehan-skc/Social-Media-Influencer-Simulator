from abc import ABC, abstractmethod

class ContentInterceptor(ABC):
    @abstractmethod
    def intercept(self, post: Post) -> Post:
        pass
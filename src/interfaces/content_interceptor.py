from abc import ABC, abstractmethod
from src.models.post import Post

class ContentInterceptor(ABC):
    @abstractmethod
    def intercept(self, post: Post) -> None:
        pass
from abc import ABC, abstractmethod

from src.models.post import Post


class ContentInterceptor(ABC):
    """
    Abstract base class for all content interceptors.
    """
    @abstractmethod
    def intercept(self, post: Post) -> None:
        pass

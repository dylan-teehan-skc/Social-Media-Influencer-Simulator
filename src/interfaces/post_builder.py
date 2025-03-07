from abc import ABC, abstractmethod

from src.models.post import Post


class PostBuilder(ABC):
    """
    Abstract base class for all post builders.
    It includes the methods to set the content, author and build the post.
    """
    @abstractmethod
    def set_content(self, content: str) -> 'PostBuilder':
        pass

    @abstractmethod
    def set_author(self, author) -> 'PostBuilder':
        pass

    @abstractmethod
    def build(self) -> Post:
        pass

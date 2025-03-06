from abc import ABC, abstractmethod

from src.models.post import Post


class PostBuilder(ABC):
    @abstractmethod
    def set_content(self, content: str) -> 'PostBuilder':
        pass

    @abstractmethod
    def set_author(self, author) -> 'PostBuilder':
        pass

    @abstractmethod
    def build(self) -> Post:
        pass

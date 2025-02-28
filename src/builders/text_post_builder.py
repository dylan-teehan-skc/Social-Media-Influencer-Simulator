from typing import TYPE_CHECKING
from src.builders.post_builder import PostBuilder
from src.models.post import Post

if TYPE_CHECKING:
    from src.models.user import User

class TextPostBuilder(PostBuilder):
    def __init__(self):
        self.post = Post("")
        self._author = None

    def set_content(self, content: str) -> 'TextPostBuilder':
        self.post.content = content
        return self

    def set_author(self, author: 'User') -> 'TextPostBuilder':
        self._author = author
        return self

    def build(self) -> Post:
        if self._author:
            self.post.author = self._author
        return self.post 
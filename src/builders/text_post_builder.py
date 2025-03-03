from typing import TYPE_CHECKING
from src.builders.post_builder import PostBuilder
from src.models.post import Post
from src.services.logger_service import LoggerService

if TYPE_CHECKING:
    from src.models.user import User

class TextPostBuilder(PostBuilder):
    def __init__(self):
        self.post = Post("")
        self._author = None
        self.logger = LoggerService.get_logger()
        self.logger.debug("Initialized TextPostBuilder")

    def set_content(self, content: str) -> 'TextPostBuilder':
        self.post.content = content
        self.logger.debug("Set text post content: %s", content[:50] + "..." if len(content) > 50 else content)
        return self

    def set_author(self, author: 'User') -> 'TextPostBuilder':
        self._author = author
        self.logger.debug("Set text post author: %s", author.handle)
        return self

    def build(self) -> Post:
        if self._author:
            self.post.author = self._author
        self.logger.info("Built text post for author %s", self._author.handle if self._author else "Unknown")
        return self.post 
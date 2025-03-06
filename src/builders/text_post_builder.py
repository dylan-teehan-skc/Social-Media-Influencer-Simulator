from typing import TYPE_CHECKING
from src.interfaces.post_builder import PostBuilder
from src.models.post import Post
from src.services.logger_service import LoggerService

if TYPE_CHECKING:
    from src.models.user import User

class TextPostBuilder(PostBuilder):
    def __init__(self):
        self.post = Post._create("")
        self._author = None
        self._image_path = None
        self.logger = LoggerService.get_logger()
        self.logger.debug("Initialized TextPostBuilder")

    def set_content(self, content: str) -> 'TextPostBuilder':
        self.post.content = content
        self.logger.debug("TextPostBuilder: Set content: %s", content[:50] + "..." if len(content) > 50 else content)
        return self

    def set_author(self, author: 'User') -> 'TextPostBuilder':
        self._author = author
        self.logger.debug("TextPostBuilder: Set author: %s", author.handle)
        return self

    def set_image(self, image_path: str) -> 'TextPostBuilder':
        self._image_path = image_path
        self.logger.debug("TextPostBuilder: Set image path: %s", image_path)
        return self

    def build(self) -> Post:
        if self._author:
            self.post.author = self._author
        if self._image_path:
            self.post.image_path = self._image_path
        self.logger.info("TextPostBuilder: Built post for author %s with content length %d", 
                        self._author.handle if self._author else "Unknown",
                        len(self.post.content))
        return self.post 
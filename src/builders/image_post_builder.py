from typing import TYPE_CHECKING
from src.interfaces.post_builder import PostBuilder
from src.models.post import Post
from src.services.logger_service import LoggerService

if TYPE_CHECKING:
    from src.models.user import User

class ImagePostBuilder(PostBuilder):
    def __init__(self):
        self.post = Post._create("")
        self._author = None
        self._image_path = None
        self.logger = LoggerService.get_logger()
        self.logger.debug("Initialized ImagePostBuilder")

    def set_content(self, content: str) -> 'ImagePostBuilder':
        self.post.content = content
        self.logger.debug("ImagePostBuilder: Set content: %s", content[:50] + "..." if len(content) > 50 else content)
        return self

    def set_author(self, author: 'User') -> 'ImagePostBuilder':
        self._author = author
        self.logger.debug("ImagePostBuilder: Set author: %s", author.handle)
        return self

    def set_image(self, image_path: str) -> 'ImagePostBuilder':
        self._image_path = image_path
        self.logger.debug("ImagePostBuilder: Set image path: %s", image_path)
        return self

    def build(self) -> Post:
        if self._author:
            self.post.author = self._author
        if self._image_path:
            self.post.image_path = self._image_path
            self.logger.info("ImagePostBuilder: Built post for author %s with content length %d and image: %s", 
                           self._author.handle if self._author else "Unknown",
                           len(self.post.content),
                           self._image_path)
        else:
            self.logger.warning("ImagePostBuilder: Building post without an image!")
        return self.post 
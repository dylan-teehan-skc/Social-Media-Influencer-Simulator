from typing import TYPE_CHECKING

from src.builders.base_post_builder import BasePostBuilder
from src.models.post import Post
from src.services.logger_service import LoggerService

if TYPE_CHECKING:
    from src.models.user import User


class TextPostBuilder(BasePostBuilder):
    """
    Builder for creating text posts.
    implements the PostBuilder interface.

    methods:
    -set_content : sets the text content of the post.
    -set_author : sets the author of the post.
    -build : builds the post and returns it.
    """
    def __init__(self):
        super().__init__("TextPostBuilder")
        self.logger = LoggerService.get_logger()
        self.logger.debug("Initialized TextPostBuilder")

    def set_content(self, content: str) -> 'TextPostBuilder':
        return super().set_content(content)

    def set_author(self, author: 'User') -> 'TextPostBuilder':
        return super().set_author(author)

    def set_image(self, image_path: str) -> 'TextPostBuilder':
        return super().set_image(image_path)

    def build(self) -> Post:
        self._apply_common_attributes()
        self.logger.info("TextPostBuilder: Built post for author %s with content length %d",
                         self._author.handle if self._author else "Unknown",
                         len(self.post.content))
        return self.post

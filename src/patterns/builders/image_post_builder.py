from typing import TYPE_CHECKING

from src.models.post import Post
from src.patterns.builders.base_post_builder import BasePostBuilder
from src.services.logger_service import LoggerService

if TYPE_CHECKING:
    from src.models.user import User


class ImagePostBuilder(BasePostBuilder):
    # Builder for creating posts with images

    def __init__(self):
        super().__init__("ImagePostBuilder")
        self.logger = LoggerService.get_logger()
        self.logger.debug("Initialized ImagePostBuilder")

    def set_content(self, content: str) -> "ImagePostBuilder":
        # Override to maintain correct return type
        return super().set_content(content)

    def set_author(self, author: "User") -> "ImagePostBuilder":
        # Override to maintain correct return type
        return super().set_author(author)

    def set_image(self, image_path: str) -> "ImagePostBuilder":
        # Override to maintain correct return type
        return super().set_image(image_path)

    def build(self) -> Post:
        # Build and return the final image post
        self._apply_common_attributes()
        if not self._image_path:
            self.logger.warning(
                "ImagePostBuilder: Building post without an image!"
            )
        else:
            self.logger.info(
                "ImagePostBuilder: Built post for author %s with content length %d and image: %s",
                self._author.handle if self._author else "Unknown",
                len(self.post.content),
                self._image_path,
            )
        return self.post

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from src.models.post import Post
from src.patterns.interfaces.post_builder import PostBuilder
from src.services.logger_service import LoggerService

if TYPE_CHECKING:
    from src.models.user import User


class BasePostBuilder(PostBuilder, ABC):
    # Base builder class for creating posts with fluent interface

    def __init__(self, builder_name: str):
        # Initialize with builder name for logging
        self.post = Post._create("")
        self._author = None
        self._image_path = None
        self.logger = LoggerService.get_logger()
        self.builder_name = builder_name
        self.logger.debug(f"Initialized {self.builder_name}")

    def set_content(self, content: str) -> "BasePostBuilder":
        # Set post content and return self for chaining
        self.post.content = content
        self.logger.debug(
            f"{self.builder_name}: Set content: %s",
            content[:50] + "..." if len(content) > 50 else content,
        )
        return self

    def set_author(self, author: "User") -> "BasePostBuilder":
        # Set post author and return self for chaining
        self._author = author
        self.logger.debug(
            f"{self.builder_name}: Set author: %s", author.handle
        )
        return self

    def set_image(self, image_path: str) -> "BasePostBuilder":
        # Set post image path and return self for chaining
        self._image_path = image_path
        self.logger.debug(
            f"{self.builder_name}: Set image path: %s", image_path
        )
        return self

    def _apply_common_attributes(self):
        # Apply author and image attributes to the post
        if self._author:
            self.post.author = self._author
        if self._image_path:
            self.post.image_path = self._image_path

    @abstractmethod
    def build(self) -> Post:
        # Implement in concrete builders to create the final post
        pass

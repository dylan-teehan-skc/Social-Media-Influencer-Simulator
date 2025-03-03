from src.builders.post_builder import PostBuilder
from src.models.post import Post
from src.models.user import User
from src.services.logger_service import LoggerService

class ImagePostBuilder(PostBuilder):
    def __init__(self):
        self.post = Post("")
        self.logger = LoggerService.get_logger()
        self.logger.debug("Initialized ImagePostBuilder")

    def set_content(self, content: str) -> 'ImagePostBuilder':
        self.post.content = f"Image: {content}"
        self.logger.debug("Set image post content with path: %s", content)
        return self

    def set_author(self, author: User) -> 'ImagePostBuilder':
        self.post.author = author
        self.logger.debug("Set image post author: %s", author.handle)
        return self

    def build(self) -> Post:
        self.logger.info("Built image post for author %s", self.post.author.handle if self.post.author else "Unknown")
        return self.post 
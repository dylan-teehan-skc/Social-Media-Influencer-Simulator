from src.builders.post_builder import PostBuilder
from src.models.post import Post
from src.models.user import User

class ImagePostBuilder(PostBuilder):
    def __init__(self):
        self.post = Post("")

    def set_content(self, content: str) -> 'ImagePostBuilder':
        self.post.content = f"Image: {content}"
        return self

    def set_author(self, author: User) -> 'ImagePostBuilder':
        self.post.author = author
        return self

    def build(self) -> Post:
        return self.post 
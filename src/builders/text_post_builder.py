from src.builders.post_builder import PostBuilder
from src.models.post import Post
from src.models.user import User

class TextPostBuilder(PostBuilder):
    def __init__(self):
        self.post = Post("")

    def set_content(self, content: str) -> 'TextPostBuilder':
        self.post.content = content
        return self

    def set_author(self, author: User) -> 'TextPostBuilder':
        self.post.author = author
        return self

    def build(self) -> Post:
        return self.post 
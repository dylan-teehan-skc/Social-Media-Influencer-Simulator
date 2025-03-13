from src.patterns.builders.text_post_builder import TextPostBuilder
from src.patterns.builders.image_post_builder import ImagePostBuilder
from src.services.logger_service import LoggerService
from src.models.post import Post

class PostBuilderFactory:
    """Factory for creating post builders."""
    
    @staticmethod
    def get_builder(post_type):
        """Get a builder for the specified post type."""
        if post_type == "text":
            return TextPostBuilder()
        elif post_type == "image":
            return ImagePostBuilder()
        else:
            raise ValueError(f"Unknown post type: {post_type}")


class BasePostBuilder:
    """Base class for post builders."""
    
    def __init__(self):
        """Initialize the builder."""
        self._content = None
        self._author = None
        self._image_path = None
        self.logger = LoggerService.get_logger()
        
    def set_content(self, content):
        """Set the post content."""
        self._content = content
        return self
        
    def set_author(self, author):
        """Set the post author."""
        self._author = author
        return self
        
    def set_image_path(self, image_path):
        """Set the post image path."""
        self._image_path = image_path
        return self
        
    def set_sentiment(self, sentiment):
        """Set the post sentiment."""
        self._sentiment = sentiment
        return self
        
    def build(self):
        """Build and return the post."""
        post = Post(self._content, self._author, self._image_path)
        
        # Set sentiment if it has been provided
        if hasattr(self, '_sentiment'):
            post.sentiment = self._sentiment
            self.logger.info(f"Set post sentiment to {self._sentiment.name} during build")
        
        return post


class TextPostBuilder(BasePostBuilder):
    """Builder for text posts."""
    
    def build(self):
        """Build and return a text post."""
        post = super().build()
        self.logger.info(f"TextPostBuilder: Built post for author {post.author.handle if post.author else 'None'} with content length {len(post.content)}")
        return post


class ImagePostBuilder(BasePostBuilder):
    """Builder for image posts."""
    
    def build(self):
        """Build and return an image post."""
        if not self._image_path:
            raise ValueError("Image path is required for image posts")
            
        post = super().build()
        self.logger.info(f"ImagePostBuilder: Built post for author {post.author.handle if post.author else 'None'} with image {self._image_path}")
        return post

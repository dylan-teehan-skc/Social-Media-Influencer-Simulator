import unittest
from unittest.mock import MagicMock, patch

from src.builders.text_post_builder import TextPostBuilder
from src.builders.image_post_builder import ImagePostBuilder
from src.factory.post_builder_factory import PostBuilderFactory
from src.models.post import Post
from src.models.user import User


class TestPostBuilder(unittest.TestCase):
    def setUp(self):
        # Create mock user
        self.mock_user = MagicMock(spec=User)
        self.mock_user.handle = "test_user"
        
        # Create test content
        self.test_content = "This is a test post content"
        self.test_image_path = "path/to/test/image.jpg"
        
        # Patch Post._create to return a mock post
        self.post_create_patcher = patch('src.models.post.Post._create')
        self.mock_post_create = self.post_create_patcher.start()
        self.mock_post = MagicMock(spec=Post)
        
        # Add necessary attributes to the mock post
        self.mock_post.author = None
        self.mock_post.image_path = None
        
        self.mock_post_create.return_value = self.mock_post

    def tearDown(self):
        self.post_create_patcher.stop()

    def test_text_post_builder(self):
        """Check if we can build a text post."""
        # Create builder
        builder = TextPostBuilder()
        
        # Set content and author
        builder.set_content(self.test_content)
        builder.set_author(self.mock_user)
        
        # Build post
        post = builder.build()
        
        # Check if Post._create was called
        self.mock_post_create.assert_called_once()
        
        # Check if post attributes were set
        self.assertEqual(post.author, self.mock_user)
        self.assertIsNone(post.image_path)
        
        # Check if the post was returned
        self.assertEqual(post, self.mock_post)

    def test_image_post_builder(self):
        """Check if we can build an image post."""
        # Create builder
        builder = ImagePostBuilder()
        
        # Set content, author, and image
        builder.set_content(self.test_content)
        builder.set_author(self.mock_user)
        builder.set_image(self.test_image_path)
        
        # Build post
        post = builder.build()
        
        # Check if Post._create was called
        self.mock_post_create.assert_called_once()
        
        # Check if post attributes were set
        self.assertEqual(post.author, self.mock_user)
        self.assertEqual(post.image_path, self.test_image_path)
        
        # Check if the post was returned
        self.assertEqual(post, self.mock_post)

    def test_image_post_builder_without_image(self):
        """Check if image post builder works even without an image."""
        # Create builder
        builder = ImagePostBuilder()
        
        # Set content and author but not image
        builder.set_content(self.test_content)
        builder.set_author(self.mock_user)
        
        # Build post
        post = builder.build()
        
        # Check if Post._create was called
        self.mock_post_create.assert_called_once()
        
        # Check if post attributes were set
        self.assertEqual(post.author, self.mock_user)
        self.assertIsNone(post.image_path)
        
        # Check if the post was returned
        self.assertEqual(post, self.mock_post)

    def test_builder_method_chaining(self):
        """Check if we can chain builder methods together."""
        # Create builder
        builder = ImagePostBuilder()
        
        # Chain methods
        post = builder.set_content(self.test_content).set_author(self.mock_user).set_image(self.test_image_path).build()
        
        # Check if Post._create was called
        self.mock_post_create.assert_called_once()
        
        # Check if post attributes were set
        self.assertEqual(post.author, self.mock_user)
        self.assertEqual(post.image_path, self.test_image_path)
        
        # Check if the post was returned
        self.assertEqual(post, self.mock_post)

    def test_post_builder_factory(self):
        """Check if the factory returns the right builder types."""
        # Get text builder
        text_builder = PostBuilderFactory.get_builder("text")
        self.assertIsInstance(text_builder, TextPostBuilder)
        
        # Get image builder
        image_builder = PostBuilderFactory.get_builder("image")
        self.assertIsInstance(image_builder, ImagePostBuilder)
        
        # Check if it rejects invalid types
        with self.assertRaises(ValueError):
            PostBuilderFactory.get_builder("invalid")


if __name__ == '__main__':
    unittest.main() 
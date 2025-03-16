import unittest
from unittest.mock import MagicMock

from src.models.post import Post
from src.models.user import User
from src.patterns.builders.image_post_builder import ImagePostBuilder
from src.patterns.builders.text_post_builder import TextPostBuilder
from src.services.logger_service import LoggerService


class TestPostBuilder(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        # Create mock user
        self.mock_user = MagicMock(spec=User)
        self.mock_user.handle = "test_user"

        # Create test content
        self.test_content = "This is a test post content"
        self.test_image_path = "path/to/test/image.jpg"

        # Create a mock post
        self.mock_post = MagicMock(spec=Post)
        self.mock_post.author = None
        self.mock_post.image_path = None

        # Create a mock logger
        self.mock_logger = MagicMock()
        LoggerService._logger = self.mock_logger

    def test_text_post_builder(self):
        """Check if we can build a text post."""
        # Create builder
        builder = TextPostBuilder()

        # Set content and author
        builder.set_content(self.test_content)
        builder.set_author(self.mock_user)

        # Build post
        post = builder.build()

        # Check if post attributes were set
        self.assertEqual(post.content, self.test_content)
        self.assertEqual(post.author, self.mock_user)
        self.assertIsNone(post.image_path)

        # Verify logging occurred
        self.mock_logger.debug.assert_any_call("Initialized TextPostBuilder")
        self.mock_logger.debug.assert_any_call(
            "TextPostBuilder: Set content: %s", self.test_content
        )
        self.mock_logger.debug.assert_any_call(
            "TextPostBuilder: Set author: %s", self.mock_user.handle
        )

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

        # Check if post attributes were set
        self.assertEqual(post.content, self.test_content)
        self.assertEqual(post.author, self.mock_user)
        self.assertEqual(post.image_path, self.test_image_path)

        # Verify logging occurred
        self.mock_logger.debug.assert_any_call("Initialized ImagePostBuilder")
        self.mock_logger.debug.assert_any_call(
            "ImagePostBuilder: Set content: %s", self.test_content
        )
        self.mock_logger.debug.assert_any_call(
            "ImagePostBuilder: Set author: %s", self.mock_user.handle
        )
        self.mock_logger.debug.assert_any_call(
            "ImagePostBuilder: Set image path: %s", self.test_image_path
        )

    def test_image_post_builder_without_image(self):
        """Check if image post builder works even without an image."""
        # Create builder
        builder = ImagePostBuilder()

        # Set content and author but not image
        builder.set_content(self.test_content)
        builder.set_author(self.mock_user)

        # Build post
        post = builder.build()

        # Check if post attributes were set
        self.assertEqual(post.content, self.test_content)
        self.assertEqual(post.author, self.mock_user)
        self.assertIsNone(post.image_path)

        # Verify logging occurred
        self.mock_logger.debug.assert_any_call("Initialized ImagePostBuilder")
        self.mock_logger.debug.assert_any_call(
            "ImagePostBuilder: Set content: %s", self.test_content
        )
        self.mock_logger.debug.assert_any_call(
            "ImagePostBuilder: Set author: %s", self.mock_user.handle
        )

    def test_builder_method_chaining(self):
        """Check if we can chain builder methods together."""
        # Create builder
        builder = ImagePostBuilder()

        # Chain methods
        post = (
            builder.set_content(self.test_content)
            .set_author(self.mock_user)
            .set_image(self.test_image_path)
            .build()
        )

        # Check if post attributes were set
        self.assertEqual(post.content, self.test_content)
        self.assertEqual(post.author, self.mock_user)
        self.assertEqual(post.image_path, self.test_image_path)

        # Verify logging occurred in the correct order
        expected_calls = [
            unittest.mock.call("Initialized ImagePostBuilder"),
            unittest.mock.call(
                "ImagePostBuilder: Set content: %s", self.test_content
            ),
            unittest.mock.call(
                "ImagePostBuilder: Set author: %s", self.mock_user.handle
            ),
            unittest.mock.call(
                "ImagePostBuilder: Set image path: %s", self.test_image_path
            ),
        ]
        self.mock_logger.debug.assert_has_calls(
            expected_calls, any_order=False
        )


if __name__ == "__main__":
    unittest.main()

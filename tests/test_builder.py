import unittest
from unittest.mock import MagicMock
from src.factory.post_builder_factory import PostBuilderFactory
from src.models.post import Sentiment
from src.models.user import User

class TestBuilder(unittest.TestCase):
    def setUp(self):
        self.text_builder = PostBuilderFactory.get_builder("text")
        self.image_builder = PostBuilderFactory.get_builder("image")
        self.user = User("test_user", "Test bio")

    def test_text_post_builder(self):
        # Test basic text post creation
        post = self.text_builder.set_content("Test content").build()
        self.assertEqual(post.content, "Test content")
        self.assertIsNone(post.image_path)

        # Test with author
        post = self.text_builder.set_content("Test content").set_author(self.user).build()
        self.assertEqual(post.author.handle, "test_user")

    def test_image_post_builder(self):
        # Test image post creation
        post = (self.image_builder
               .set_content("Test image post")
               .set_image_path("test.png")
               .build())
        self.assertEqual(post.content, "Test image post")
        self.assertEqual(post.image_path, "test.png")

    def test_builder_reset(self):
        # Build first post
        first_post = (self.text_builder
                     .set_content("First post")
                     .set_author(self.user)
                     .build())
        
        # Build second post with same builder
        second_post = self.text_builder.set_content("Second post").build()
        
        # Verify posts are different
        self.assertNotEqual(first_post.content, second_post.content)
        self.assertIsNone(second_post.author)  # Author should be reset

    def test_invalid_builder_type(self):
        with self.assertRaises(ValueError):
            PostBuilderFactory.get_builder("invalid_type")

    def test_builder_chaining(self):
        # Test method chaining
        post = (self.text_builder
                .set_content("Chain test")
                .set_author(self.user)
                .build())
        
        self.assertEqual(post.content, "Chain test")
        self.assertEqual(post.author.handle, "test_user")

if __name__ == '__main__':
    unittest.main() 
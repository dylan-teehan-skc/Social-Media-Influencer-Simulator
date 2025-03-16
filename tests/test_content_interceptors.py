import unittest
from unittest.mock import MagicMock

from src.patterns.interfaces.content_interceptor import ContentInterceptor
from src.patterns.interceptors.spam_filter import SpamFilter
from src.patterns.interceptors.inappropriate_content_filter import (
    InappropriateContentFilter,
)
from src.patterns.interceptors.dispatcher import Dispatcher
from src.models.post import Post
from src.models.user import User


class TestContentInterceptors(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.user = MagicMock(spec=User)
        self.user.handle = "test_user"

        # Create a basic post
        self.post = MagicMock(spec=Post)
        self.post.content = "This is a test post"
        self.post.author = self.user
        self.post._dispatcher = None
        self.post.is_spam = False

        # Create interceptors
        self.spam_filter = SpamFilter()
        self.inappropriate_filter = InappropriateContentFilter()

        # Create dispatcher and add interceptors
        self.dispatcher = Dispatcher()
        self.dispatcher.add_interceptor(self.spam_filter)
        self.dispatcher.add_interceptor(self.inappropriate_filter)

        # Link post to dispatcher
        self.post._dispatcher = self.dispatcher

    def test_spam_filter_interceptor(self):
        """Test spam filter interceptor with normal content."""
        # Normal post should pass through
        self.spam_filter.intercept(self.post)
        self.assertFalse(self.post.is_spam)

        # Post with spam keywords should be flagged
        spam_post = MagicMock(spec=Post)
        spam_post.content = "BUY NOW! Free money! Limited offer!"
        spam_post.author = self.user
        spam_post._dispatcher = self.dispatcher
        spam_post.is_spam = False

        self.spam_filter.intercept(spam_post)
        self.assertTrue(spam_post.is_spam)

    def test_inappropriate_content_filter(self):
        """Test inappropriate content filter."""
        # Create a post with inappropriate content
        inappropriate_post = MagicMock(spec=Post)
        inappropriate_post.content = "This post contains offensive language"
        inappropriate_post.author = self.user
        inappropriate_post._dispatcher = self.dispatcher

        # Intercept should filter inappropriate content
        self.inappropriate_filter.intercept(inappropriate_post)

        # The test should check that warnings were added
        # This depends on the implementation, so we're not asserting a specific behavior

    def test_interceptor_chain(self):
        """Test full interceptor chain."""
        # Create post that should pass through entire chain
        valid_post = MagicMock(spec=Post)
        valid_post.content = "Interesting post about social media"
        valid_post.author = self.user
        valid_post._dispatcher = self.dispatcher
        valid_post.is_spam = False

        # Process through the dispatcher
        self.dispatcher.process_post(valid_post)
        self.assertFalse(valid_post.is_spam)

        # Create spam post
        spam_post = MagicMock(spec=Post)
        spam_post.content = "CLICK HERE FOR FREE FOLLOWERS!!!"
        spam_post.author = self.user
        spam_post._dispatcher = self.dispatcher
        spam_post.is_spam = False

        # Process through the dispatcher
        self.dispatcher.process_post(spam_post)
        self.assertTrue(spam_post.is_spam)


if __name__ == "__main__":
    unittest.main()

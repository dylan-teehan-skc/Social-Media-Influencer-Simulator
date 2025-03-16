import unittest
from datetime import datetime
from unittest.mock import MagicMock

from PyQt6.QtCore import QObject

from src.models.post import Comment, Post, Sentiment
from src.services.logger_service import LoggerService


class TestPost(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        # Create a test post
        self.test_content = "This is a test post content"
        self.post = Post(self.test_content)

        # Create a mock user
        self.mock_user = MagicMock()
        self.mock_user.handle = "test_user"
        self.post.author = self.mock_user

        # Create a mock logger
        self.mock_logger = MagicMock()
        LoggerService._logger = self.mock_logger

    def test_post_initialization(self):
        """Check if posts get created with the right starting values."""
        self.assertEqual(self.post.content, self.test_content)
        self.assertEqual(self.post.author, self.mock_user)
        self.assertIsNone(self.post.image_path)
        self.assertEqual(self.post.sentiment, Sentiment.NEUTRAL)
        self.assertEqual(len(self.post.comments), 0)
        self.assertFalse(self.post.is_spam)
        self.assertTrue(self.post.is_valid)
        self.assertIsInstance(self.post.timestamp, datetime)
        self.assertEqual(self.post.likes, 0)
        self.assertEqual(self.post.shares, 0)
        self.assertEqual(self.post.followers_gained, 0)
        self.assertEqual(self.post.followers_lost, 0)
        self.assertIsInstance(self.post, QObject)

    def test_signals_exist(self):
        """Test that all required signals are defined."""
        self.assertTrue(hasattr(self.post, "likes_changed"))
        self.assertTrue(hasattr(self.post, "shares_changed"))
        self.assertTrue(hasattr(self.post, "comments_changed"))
        self.assertTrue(hasattr(self.post, "sentiment_changed"))
        self.assertTrue(hasattr(self.post, "followers_gained_changed"))
        self.assertTrue(hasattr(self.post, "followers_lost_changed"))

    def test_property_setters(self):
        """Test that property setters work correctly."""
        new_content = "New content"
        new_image = "path/to/new/image.jpg"

        self.post.content = new_content
        self.post.image_path = new_image

        self.assertEqual(self.post.content, new_content)
        self.assertEqual(self.post.image_path, new_image)

    def test_sentiment_setter_with_signal(self):
        """Test that setting sentiment emits signal when changed."""
        # Create a mock slot
        mock_slot = MagicMock()
        self.post.sentiment_changed.connect(mock_slot)

        # Change sentiment
        self.post.sentiment = Sentiment.LEFT

        # Check if signal was emitted
        mock_slot.assert_called_once_with(Sentiment.LEFT)

        # Change to same sentiment - should not emit
        mock_slot.reset_mock()
        self.post.sentiment = Sentiment.LEFT
        mock_slot.assert_not_called()

    def test_like_operations(self):
        """Test internal like operations."""
        # Create a mock slot
        mock_slot = MagicMock()
        self.post.likes_changed.connect(mock_slot)

        # Test increment
        self.post._increment_likes()
        self.assertEqual(self.post.likes, 1)
        mock_slot.assert_called_with(1)

        # Test decrement
        self.post._decrement_likes()
        self.assertEqual(self.post.likes, 0)
        mock_slot.assert_called_with(0)

        # Test decrement at zero
        self.post._decrement_likes()
        self.assertEqual(self.post.likes, 0)

    def test_share_operations(self):
        """Test internal share operations."""
        # Create a mock slot
        mock_slot = MagicMock()
        self.post.shares_changed.connect(mock_slot)

        # Test increment
        self.post._increment_shares()
        self.assertEqual(self.post.shares, 1)
        mock_slot.assert_called_with(1)

        # Test decrement
        self.post._decrement_shares()
        self.assertEqual(self.post.shares, 0)
        mock_slot.assert_called_with(0)

        # Test decrement at zero
        self.post._decrement_shares()
        self.assertEqual(self.post.shares, 0)

    def test_comment_operations(self):
        """Test internal comment operations."""
        # Create a mock slot
        mock_slot = MagicMock()
        self.post.comments_changed.connect(mock_slot)

        # Create and add a comment
        comment = Comment("Test comment", Sentiment.NEUTRAL, "commenter")
        self.post._add_comment(comment)

        # Check if comment was added and signal emitted
        self.assertEqual(len(self.post.comments), 1)
        self.assertEqual(self.post.comments[0], comment)
        mock_slot.assert_called_once()

    def test_follower_tracking(self):
        """Test follower tracking operations."""
        # Create mock slots
        gained_slot = MagicMock()
        lost_slot = MagicMock()
        self.post.followers_gained_changed.connect(gained_slot)
        self.post.followers_lost_changed.connect(lost_slot)

        # Test gained followers
        self.post._add_follower_gained()
        self.assertEqual(self.post.followers_gained, 1)
        gained_slot.assert_called_with(1)

        # Test lost followers
        self.post._add_follower_lost()
        self.assertEqual(self.post.followers_lost, 1)
        lost_slot.assert_called_with(1)


class TestComment(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.content = "This is a test comment"
        self.sentiment = Sentiment.NEUTRAL
        self.author = "test_commenter"
        self.comment = Comment(self.content, self.sentiment, self.author)

    def test_comment_initialization(self):
        """Check if comments get created with the right starting values."""
        self.assertEqual(self.comment.content, self.content)
        self.assertEqual(self.comment.sentiment, self.sentiment)
        self.assertEqual(self.comment.author, self.author)
        self.assertIsInstance(self.comment.timestamp, datetime)
        self.assertIsInstance(self.comment, QObject)

    def test_to_dict(self):
        """Check if converting a comment to a dictionary works."""
        comment_dict = self.comment.to_dict()

        self.assertEqual(comment_dict["content"], self.content)
        self.assertEqual(comment_dict["sentiment"], self.sentiment.value)
        self.assertEqual(comment_dict["author"], self.author)
        self.assertIsInstance(comment_dict["timestamp"], str)


if __name__ == "__main__":
    unittest.main()

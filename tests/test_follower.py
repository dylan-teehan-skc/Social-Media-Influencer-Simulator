import unittest
from unittest.mock import MagicMock

from PyQt6.QtCore import QObject

from src.models.follower import Follower
from src.models.post import Post, Sentiment
from src.models.user import User
from src.patterns.command.command_history import CommandHistory
from src.services.logger_service import LoggerService


class TestFollower(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        # Create followers with different political leanings
        self.left_follower = Follower(Sentiment.LEFT, "left_follower_1234")
        self.right_follower = Follower(Sentiment.RIGHT, "right_follower_5678")
        self.neutral_follower = Follower(
            Sentiment.NEUTRAL, "neutral_follower_9012"
        )

        # Create a mock post
        self.mock_post = MagicMock(spec=Post)
        self.mock_post.sentiment = Sentiment.NEUTRAL
        self.mock_post.comments = []
        self.mock_post.author = MagicMock()
        self.mock_post.author.handle = "test_author"

        # Create a mock user
        self.mock_user = MagicMock(spec=User)

        # Create a mock logger
        self.mock_logger = MagicMock()
        LoggerService._logger = self.mock_logger

    def test_follower_initialization(self):
        """Check if followers get created with the right starting values."""
        # Check left-leaning follower
        self.assertEqual(self.left_follower.handle, "left_follower_1234")
        self.assertEqual(self.left_follower.sentiment, Sentiment.LEFT)
        self.assertLessEqual(self.left_follower.political_lean, 30)
        self.assertIsInstance(self.left_follower, QObject)
        self.assertIsInstance(
            self.left_follower.command_history, CommandHistory
        )

        # Check right-leaning follower
        self.assertEqual(self.right_follower.handle, "right_follower_5678")
        self.assertEqual(self.right_follower.sentiment, Sentiment.RIGHT)
        self.assertGreaterEqual(self.right_follower.political_lean, 70)

        # Check neutral follower
        self.assertEqual(self.neutral_follower.handle, "neutral_follower_9012")
        self.assertEqual(self.neutral_follower.sentiment, Sentiment.NEUTRAL)
        self.assertGreaterEqual(self.neutral_follower.political_lean, 40)
        self.assertLessEqual(self.neutral_follower.political_lean, 60)

    def test_signals_exist(self):
        """Test that all required signals are defined."""
        self.assertTrue(hasattr(self.left_follower, "interaction_occurred"))
        self.assertTrue(hasattr(self.left_follower, "unfollowed"))

    def test_create_with_random_handle(self):
        """Check if we can create a follower with a random handle."""
        follower = Follower.create_with_random_handle(Sentiment.LEFT)
        self.assertEqual(follower.sentiment, Sentiment.LEFT)
        self.assertTrue(
            any(
                prefix in follower.handle
                for prefix in Follower.FOLLOWER_PREFIXES["LEFT"]
            )
        )
        self.assertRegex(follower.handle, r"[a-z_]+\d{4}")

    def test_create_random_follower(self):
        """Check if we can create random followers based on index."""
        # Index 0 should be LEFT
        follower0 = Follower.create_random_follower(0)
        self.assertEqual(follower0.sentiment, Sentiment.LEFT)

        # Index 1 should be RIGHT
        follower1 = Follower.create_random_follower(1)
        self.assertEqual(follower1.sentiment, Sentiment.RIGHT)

        # Index 2 should be NEUTRAL
        follower2 = Follower.create_random_follower(2)
        self.assertEqual(follower2.sentiment, Sentiment.NEUTRAL)

        # Index 3 should cycle back to LEFT
        follower3 = Follower.create_random_follower(3)
        self.assertEqual(follower3.sentiment, Sentiment.LEFT)

    def test_political_lean_setter(self):
        """Test that political lean setter works correctly."""
        # Test setting within bounds
        self.left_follower.political_lean = 50
        self.assertEqual(self.left_follower.political_lean, 50)

        # Test setting below minimum
        self.left_follower.political_lean = -10
        self.assertEqual(self.left_follower.political_lean, 0)

        # Test setting above maximum
        self.left_follower.political_lean = 110
        self.assertEqual(self.left_follower.political_lean, 100)

    def test_update_method(self):
        """Test the update method behavior."""
        # Set up mock slot for interaction_occurred signal
        mock_slot = MagicMock()
        self.left_follower.interaction_occurred.connect(mock_slot)

        # Call update with a post
        result = self.left_follower.update(self.mock_user, self.mock_post)

        # Check that interaction_occurred signal was emitted
        mock_slot.assert_called_once()

        # Check that update returns False by default
        self.assertFalse(result)

    def test_interact_with_post_alignment(self):
        """Test post interaction alignment calculations."""
        # Test left-leaning follower with different post types
        self.left_follower.political_lean = 20  # Strong left lean

        # Test with left post (should have high alignment)
        self.mock_post.sentiment = Sentiment.LEFT
        self.left_follower.interact_with_post(self.mock_post)

        # Test with right post (should have low alignment)
        self.mock_post.sentiment = Sentiment.RIGHT
        self.left_follower.interact_with_post(self.mock_post)

        # Test with neutral post (should have moderate alignment)
        self.mock_post.sentiment = Sentiment.NEUTRAL
        self.left_follower.interact_with_post(self.mock_post)

        # Verify that interaction_occurred was emitted each time
        mock_slot = MagicMock()
        self.left_follower.interaction_occurred.connect(mock_slot)
        self.left_follower.interact_with_post(self.mock_post)
        mock_slot.assert_called_once_with(self.left_follower, self.mock_post)


if __name__ == "__main__":
    unittest.main()

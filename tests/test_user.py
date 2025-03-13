import unittest
from unittest.mock import MagicMock, patch
from PyQt6.QtCore import QObject

from src.models.user import User
from src.models.post import Post, Comment
from src.models.sentiment import Sentiment
from src.models.follower import Follower
from datetime import datetime


class TestUser(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.user = User("test_user", "Test user bio")
        
        # Set up some mock followers with different political leanings
        self.left_follower = Follower(Sentiment.LEFT, "left_follower")
        self.right_follower = Follower(Sentiment.RIGHT, "right_follower")
        self.neutral_follower = Follower(Sentiment.NEUTRAL, "neutral_follower")

    def test_user_initialization(self):
        """Check if user gets created with the right starting values."""
        self.assertEqual(self.user.handle, "test_user")
        self.assertEqual(self.user.bio, "Test user bio")
        self.assertEqual(len(self.user.followers), 0)
        self.assertEqual(self.user.follower_count, 0)
        self.assertEqual(len(self.user.posts), 0)
        self.assertEqual(self.user.recent_follower_losses, 0)
        self.assertIsInstance(self.user, QObject)

    def test_attach_observer(self):
        """Make sure we can add followers to a user."""
        self.user.attach(self.left_follower)
        self.assertEqual(len(self.user._observers), 1)
        self.assertIn(self.left_follower, self.user._observers)

    def test_detach_observer(self):
        """Make sure we can remove followers from a user."""
        self.user.attach(self.left_follower)
        self.user.detach(self.left_follower)
        self.assertEqual(len(self.user._observers), 0)
        self.assertNotIn(self.left_follower, self.user._observers)

    def test_notify_observers(self):
        """Test that observers are notified correctly."""
        mock_observer = MagicMock()
        mock_post = MagicMock()
        
        self.user.attach(mock_observer)
        self.user.notify(mock_post)
        
        mock_observer.update.assert_called_once_with(self.user, mock_post)

    def test_property_setters(self):
        """Test the property setters work correctly."""
        new_handle = "new_handle"
        new_bio = "new bio"
        
        self.user.handle = new_handle
        self.user.bio = new_bio
        
        self.assertEqual(self.user.handle, new_handle)
        self.assertEqual(self.user.bio, new_bio)

    def test_signals(self):
        """Test that signals are defined correctly."""
        self.assertTrue(hasattr(self.user, 'follower_added'))
        self.assertTrue(hasattr(self.user, 'follower_removed'))
        self.assertTrue(hasattr(self.user, 'post_created'))
        self.assertTrue(hasattr(self.user, 'reputation_changed'))

    def test_constants(self):
        """Test that the constants are defined with correct values."""
        self.assertEqual(self.user.REPUTATION_RECOVERY_DELAY, 60000)
        self.assertEqual(self.user.MAX_REPUTATION_PENALTY, 0.5)
        self.assertEqual(self.user.REPUTATION_PENALTY_PER_LOSS, 0.1)
        self.assertEqual(self.user.REPUTATION_WARNING_THRESHOLD, 5)
        self.assertEqual(self.user.BASE_NEUTRAL_CHANCE, 20)
        self.assertEqual(self.user.HOT_TAKE_CHANCE, 30)
        self.assertEqual(self.user.MAX_FOLLOWER_MULTIPLIER, 3.0)
        self.assertEqual(self.user.FOLLOWER_MULTIPLIER_SCALE, 1000)


if __name__ == '__main__':
    unittest.main() 
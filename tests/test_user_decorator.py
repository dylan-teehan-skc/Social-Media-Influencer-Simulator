import unittest
from unittest.mock import MagicMock, patch

from src.patterns.decorator.verified_user import VerifiedUser
from src.patterns.decorator.sponsored_user import SponsoredUser
from src.models.user import User
from PyQt6.QtCore import QObject, pyqtSignal


class MockUser(QObject):
    """Mock user class that properly implements Qt signals."""
    follower_added = pyqtSignal(object)
    follower_removed = pyqtSignal(object)
    post_created = pyqtSignal(object)
    reputation_changed = pyqtSignal(int)


class TestUserDecorator(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock user with proper Qt signals
        self.mock_user = MockUser()
        
        # Add mock attributes and methods
        self.mock_user.handle = "test_user"
        self.mock_user.bio = "Test user bio"
        
        # Set up follower-related properties
        # followers: List of follower objects (used for accessing individual followers)
        self.mock_user.followers = [MagicMock() for _ in range(100)]
        # follower_count: Integer count of followers (used for quick size checks)
        self.mock_user.follower_count = 100
        
        # Set up other properties
        self.mock_user.posts = []
        self.mock_user.recent_follower_losses = 0
        
        # Configure mock methods
        self.mock_user.add_follower = MagicMock()
        self.mock_user.remove_follower = MagicMock()
        self.mock_user.create_post = MagicMock()
        self.mock_user.attach = MagicMock()
        self.mock_user.detach = MagicMock()
        self.mock_user.notify = MagicMock()
        self.mock_user.update_reputation_recovery = MagicMock()
        
        # Store original values for comparison
        self.original_handle = self.mock_user.handle
        self.original_bio = self.mock_user.bio

    def test_verified_user_decorator(self):
        """Check if verified user decorator adds the checkmark."""
        # Create a verified user
        verified_user = VerifiedUser(self.mock_user)
        
        # Check if handle gets the checkmark
        self.assertEqual(verified_user.get_handle(), "test_user ✔️")
        
        # Check if bio gets the verified tag
        self.assertEqual(verified_user.get_bio(), "Test user bio (Verified)")
        
        # Check if original user is unchanged
        self.assertEqual(self.mock_user.handle, self.original_handle)
        self.assertEqual(self.mock_user.bio, self.original_bio)

    def test_sponsored_user_decorator(self):
        """Check if sponsored user decorator adds the sponsor info."""
        # Create a sponsored user
        company_name = "Test Company"
        sponsored_user = SponsoredUser(self.mock_user, company_name)
        
        # Check if handle gets the sponsored tag
        self.assertEqual(sponsored_user.get_handle(), "test_user [Sponsored]")
        
        # Check if bio shows the sponsor
        self.assertEqual(sponsored_user.get_bio(), f"Sponsored by {company_name}")
        
        # Check if original user is unchanged
        self.assertEqual(self.mock_user.handle, self.original_handle)
        self.assertEqual(self.mock_user.bio, self.original_bio)

    def test_nested_decorators(self):
        """Check if we can stack decorators."""
        # Create a verified and sponsored user
        company_name = "Test Company"
        verified_user = VerifiedUser(self.mock_user)
        verified_sponsored_user = SponsoredUser(verified_user, company_name)
        
        # Check if handle has both decorations
        self.assertEqual(verified_sponsored_user.get_handle(), "test_user ✔️ [Sponsored]")
        
        # Check if bio shows sponsor info (last decorator takes precedence)
        self.assertEqual(verified_sponsored_user.get_bio(), f"Sponsored by {company_name}")
        
        # Check if original user is unchanged
        self.assertEqual(self.mock_user.handle, self.original_handle)
        self.assertEqual(self.mock_user.bio, self.original_bio)

    def test_verified_user_property_forwarding(self):
        """Test that properties are properly forwarded to the decorated user."""
        verified_user = VerifiedUser(self.mock_user)
        
        # Test follower_count property (integer count)
        self.assertEqual(verified_user.follower_count, 100)
        
        # Test followers property (list of follower objects)
        self.assertEqual(len(verified_user.followers), 100)
        self.assertIsInstance(verified_user.followers, list)
        self.assertTrue(all(isinstance(f, MagicMock) for f in verified_user.followers))
        
        # Test posts property
        self.assertEqual(verified_user.posts, [])
        
        # Test recent_follower_losses property
        self.assertEqual(verified_user.recent_follower_losses, 0)

    def test_verified_user_signal_forwarding(self):
        """Test that signals are properly forwarded from the decorated user."""
        verified_user = VerifiedUser(self.mock_user)
        
        # Verify that all signals exist on the verified user
        self.assertTrue(hasattr(verified_user, 'follower_added'))
        self.assertTrue(hasattr(verified_user, 'follower_removed'))
        self.assertTrue(hasattr(verified_user, 'post_created'))
        self.assertTrue(hasattr(verified_user, 'reputation_changed'))
        
        # Verify that signals are properly connected
        # Note: We can't check the exact type because PyQt signals become bound methods
        self.assertTrue(callable(verified_user.follower_added.emit))
        self.assertTrue(callable(verified_user.follower_removed.emit))
        self.assertTrue(callable(verified_user.post_created.emit))
        self.assertTrue(callable(verified_user.reputation_changed.emit))

    def test_verified_user_method_forwarding(self):
        """Test that methods are properly forwarded to the decorated user."""
        verified_user = VerifiedUser(self.mock_user)
        
        # Test add_follower
        test_follower = MagicMock()
        test_post = MagicMock()
        verified_user.add_follower(test_follower, test_post)
        self.mock_user.add_follower.assert_called_once_with(test_follower, test_post)
        
        # Test remove_follower
        verified_user.remove_follower(test_follower)
        self.mock_user.remove_follower.assert_called_once_with(test_follower)
        
        # Test create_post
        test_content = "Test post"
        test_image = "test.jpg"
        verified_user.create_post(test_content, test_image)
        self.mock_user.create_post.assert_called_once_with(test_content, test_image)
        
        # Test attach/detach/notify
        test_observer = MagicMock()
        verified_user.attach(test_observer)
        self.mock_user.attach.assert_called_once_with(test_observer)
        
        verified_user.detach(test_observer)
        self.mock_user.detach.assert_called_once_with(test_observer)
        
        verified_user.notify()
        self.mock_user.notify.assert_called_once_with()

    def test_verified_user_getattr(self):
        """Test that unknown attributes are properly forwarded via __getattr__."""
        verified_user = VerifiedUser(self.mock_user)
        
        # Add a custom attribute to the mock user
        self.mock_user.custom_attribute = "test_value"
        
        # Test that we can access the custom attribute
        self.assertEqual(verified_user.custom_attribute, "test_value")
        
        # Test that accessing a non-existent attribute raises AttributeError
        with self.assertRaises(AttributeError):
            verified_user.non_existent_attribute

    def test_verified_user_reputation_recovery(self):
        """Test that reputation recovery is properly forwarded."""
        verified_user = VerifiedUser(self.mock_user)
        test_time = 1000000
        
        verified_user.update_reputation_recovery(test_time)
        self.mock_user.update_reputation_recovery.assert_called_once_with(test_time)


if __name__ == '__main__':
    unittest.main() 
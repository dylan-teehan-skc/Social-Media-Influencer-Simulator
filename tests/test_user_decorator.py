import unittest
from unittest.mock import MagicMock

from src.patterns.decorator.verified_user import VerifiedUser
from src.patterns.decorator.sponsered_user import SponsoredUser
from src.models.user import User


class TestUserDecorator(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock user
        self.mock_user = MagicMock(spec=User)
        self.mock_user.handle = "test_user"
        self.mock_user.bio = "Test user bio"
        self.mock_user.followers = 100
        
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


if __name__ == '__main__':
    unittest.main() 
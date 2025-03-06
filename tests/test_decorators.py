import unittest
from src.models.user import User
from src.decorator.verified_user import VerifiedUser
from src.decorator.sponsered_user import SponsoredUser

class TestDecorators(unittest.TestCase):
    def setUp(self):
        self.base_user = User("test_user", "Test bio")

    def test_verified_user(self):
        verified = VerifiedUser(self.base_user)
        self.assertIn("✔️", verified.handle)
        self.assertIn("Verified", verified.bio)

    def test_sponsored_user(self):
        sponsored = SponsoredUser(self.base_user, "TestCorp")
        self.assertIn("[Sponsored]", sponsored.handle)
        self.assertIn("Sponsored by TestCorp", sponsored.bio)

    def test_multiple_decorators(self):
        # Test applying multiple decorators
        user = self.base_user
        user = VerifiedUser(user)
        user = SponsoredUser(user, "TestCorp")

        # Check that both decorations are present
        self.assertIn("✔️", user.handle)
        self.assertIn("[Sponsored]", user.handle)
        self.assertIn("Verified", user.bio)
        self.assertIn("Sponsored by TestCorp", user.bio)

    def test_decorator_order(self):
        # Test different order of decorators
        order1 = SponsoredUser(VerifiedUser(self.base_user), "TestCorp")
        order2 = VerifiedUser(SponsoredUser(self.base_user, "TestCorp"))

        # Both orders should contain all decorations
        for user in [order1, order2]:
            self.assertIn("✔️", user.handle)
            self.assertIn("[Sponsored]", user.handle)
            self.assertIn("Verified", user.bio)
            self.assertIn("Sponsored by TestCorp", user.bio)

if __name__ == '__main__':
    unittest.main() 
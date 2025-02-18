import unittest
from src.classes.post import Post

class MockFollower:
    """A mock follower class for testing purposes."""
    pass

class TestPost(unittest.TestCase):

    def test_like_post(self):
        post = Post("Test content")
        follower = MockFollower()
        post.like(follower)
        self.assertIn(follower, post.likes, "Follower should be in the likes list")

    def test_unlike_post(self):
        post = Post("Test content")
        follower = MockFollower()
        post.like(follower)
        post.unlike(follower)
        self.assertNotIn(follower, post.likes, "Follower should not be in the likes list")

    def test_share_post(self):
        post = Post("Test content")
        follower = MockFollower()
        post.share(follower)
        self.assertIn(follower, post.shares, "Follower should be in the shares list")

    def test_unshare_post(self):
        post = Post("Test content")
        follower = MockFollower()
        post.share(follower)
        post.unshare(follower)
        self.assertNotIn(follower, post.shares, "Follower should not be in the shares list")

if __name__ == '__main__':
    unittest.main() 
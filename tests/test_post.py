import unittest
from models.post import Post

class TestPost(unittest.TestCase):

    def test_like_post(self):
        post = Post("Test content")
        post.like()
        self.assertEqual(post.likes, 1, "Likes should be incremented to 1")

    def test_unlike_post(self):
        post = Post("Test content")
        post.like()
        post.unlike()
        self.assertEqual(post.likes, 0, "Likes should be decremented to 0")

    def test_share_post(self):
        post = Post("Test content")
        post.share()
        self.assertEqual(post.shares, 1, "Shares should be incremented to 1")

    def test_unshare_post(self):
        post = Post("Test content")
        post.share()
        post.unshare()
        self.assertEqual(post.shares, 0, "Shares should be decremented to 0")

if __name__ == '__main__':
    unittest.main() 
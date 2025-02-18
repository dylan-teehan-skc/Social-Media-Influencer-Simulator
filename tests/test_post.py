import unittest
from datetime import datetime
from src.classes.post import Post

class TestPost(unittest.TestCase):
    
    def test_initialization(self):
        content = "Hello, world!"
        post = Post(content)
        
        self.assertEqual(post.content, content)
        self.assertIsInstance(post.timestamp, datetime)
        self.assertEqual(post.likes, 0)
        self.assertEqual(post.shares, 0)
    
    def test_like(self):
        post = Post("Test post")
        post.like()
        self.assertEqual(post.likes, 1)
        
    def test_unlike(self):
        post = Post("Test post")
        post.like()
        post.unlike()
        self.assertEqual(post.likes, 0)
        
    def test_share(self):
        post = Post("Test post")
        post.share()
        self.assertEqual(post.shares, 1)
        
    def test_unshare(self):
        post = Post("Test post")
        post.share()
        post.unshare()
        self.assertEqual(post.shares, 0)

if __name__ == '__main__':
    unittest.main() 
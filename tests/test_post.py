import unittest
from src.models.post import Post, Sentiment, Comment

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
        
    def test_add_comment(self):
        post = Post("Test content")
        comment = Comment("Great post!", Sentiment.NEUTRAL, "user123")
        post.add_comment(comment)
        self.assertEqual(len(post.comments), 1, "Comment should be added to post")
        self.assertEqual(post.comments[0].content, "Great post!", "Comment content should match")
        
    def test_follower_tracking(self):
        post = Post("Test content")
        
        # Test follower gain
        post.add_follower_gained()
        self.assertEqual(post.followers_gained, 1, "Should track gained follower")
        
        # Test follower loss
        post.add_follower_lost()
        self.assertEqual(post.followers_lost, 1, "Should track lost follower")
        
    def test_initial_sentiment(self):
        post = Post("Test content")
        post.initial_impressions()  # This will use fallback random sentiment
        self.assertIn(post.sentiment, [Sentiment.LEFT, Sentiment.RIGHT, Sentiment.NEUTRAL], 
                     "Post should have valid sentiment")

if __name__ == '__main__':
    unittest.main() 
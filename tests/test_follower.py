import unittest
from src.models.follower import Follower
from src.models.post import Post, Sentiment, Comment
from src.factory.post_builder_factory import PostBuilderFactory

class TestFollower(unittest.TestCase):
    def setUp(self):
        self.post_builder = PostBuilderFactory.get_builder("text")

    def test_initial_sentiment_adjustment_left(self):
        follower = Follower(Sentiment.LEFT, handle="follower1")
        self.assertLessEqual(follower.political_lean, 30, "Left-leaning followers should have political lean 0-30")

    def test_initial_sentiment_adjustment_right(self):
        follower = Follower(Sentiment.RIGHT, handle="follower2")
        self.assertGreaterEqual(follower.political_lean, 70, "Right-leaning followers should have political lean 70-100")

    def test_initial_sentiment_adjustment_neutral(self):
        follower = Follower(Sentiment.NEUTRAL, handle="follower3")
        self.assertTrue(40 <= follower.political_lean <= 60, "Neutral followers should have political lean 40-60")
        
    def test_interact_with_aligned_post(self):
        follower = Follower(Sentiment.LEFT, handle="leftie")
        post = self.post_builder.set_content("Left-leaning content").build()
        post.sentiment = Sentiment.LEFT
        
        # Create a mock author for the post
        class MockAuthor:
            def __init__(self, handle):
                self.handle = handle
        
        post.author = MockAuthor("test_author")
        
        follower.interact_with_post(post)
        self.assertGreater(post.likes, 0, "Aligned followers should like the post")
        self.assertGreater(post.shares, 0, "Aligned followers should share the post")
        
    def test_interact_with_opposed_post(self):
        follower = Follower(Sentiment.LEFT, handle="leftie")
        post = self.post_builder.set_content("Right-leaning content").build()
        post.sentiment = Sentiment.RIGHT
        
        # Create a mock author for the post
        class MockAuthor:
            def __init__(self, handle):
                self.handle = handle
        
        post.author = MockAuthor("test_author")
        
        follower.interact_with_post(post)
        self.assertEqual(post.likes, 0, "Opposed followers should not like the post")
        self.assertEqual(post.shares, 0, "Opposed followers should not share the post")
        
    def test_should_unfollow_opposed_content(self):
        follower = Follower(Sentiment.LEFT, handle="leftie")
        follower.political_lean = 10  # Strongly left
        post = self.post_builder.set_content("Right-leaning content").build()
        post.sentiment = Sentiment.RIGHT
        
        # Run multiple times to account for randomness
        unfollow_occurred = False
        for _ in range(100):
            if follower._should_unfollow(post):
                unfollow_occurred = True
                break
                
        self.assertTrue(unfollow_occurred, "Strongly opposed followers should have a chance to unfollow")

if __name__ == '__main__':
    unittest.main() 
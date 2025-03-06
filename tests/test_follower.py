import unittest
from unittest.mock import MagicMock
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

    def test_adjust_lean_from_sentiment(self):
        follower = Follower(Sentiment.NEUTRAL, handle="moderate")
        initial_lean = follower.political_lean
        
        # Test right-wing content adjustment
        follower._adjust_lean_from_sentiment(Sentiment.RIGHT)
        self.assertGreaterEqual(follower.political_lean, initial_lean, 
                              "Political lean should increase or stay same for right content")
        
        # Test left-wing content adjustment
        initial_lean = follower.political_lean
        follower._adjust_lean_from_sentiment(Sentiment.LEFT)
        self.assertLessEqual(follower.political_lean, initial_lean,
                           "Political lean should decrease or stay same for left content")
        
        # Test neutral content
        initial_lean = follower.political_lean
        follower._adjust_lean_from_sentiment(Sentiment.NEUTRAL)
        self.assertEqual(follower.political_lean, initial_lean,
                        "Political lean should not change for neutral content")

    def test_get_comment_based_on_alignment(self):
        follower = Follower(Sentiment.NEUTRAL, handle="commenter")
        
        # Test positive comments (high alignment)
        comment = follower._get_comment(80)
        self.assertIn(comment, follower.positive_comments,
                     "High alignment should result in positive comment")
        
        # Test neutral comments (medium alignment)
        comment = follower._get_comment(50)
        self.assertIn(comment, follower.neutral_comments,
                     "Medium alignment should result in neutral comment")
        
        # Test negative comments (low alignment)
        comment = follower._get_comment(20)
        self.assertIn(comment, follower.negative_comments,
                     "Low alignment should result in negative comment")

    def test_command_history(self):
        follower = Follower(Sentiment.NEUTRAL, handle="historian")
        post = self.post_builder.set_content("Test content").build()
        post.sentiment = Sentiment.NEUTRAL
        post.author = MagicMock(handle="test_author")
        
        # Interact with post to generate commands
        follower.interact_with_post(post)
        
        # Check if commands were recorded
        self.assertGreater(len(follower.command_history.history), 0,
                          "Command history should record interactions")

    def test_alignment_calculation(self):
        follower = Follower(Sentiment.NEUTRAL, handle="calculator")
        post = self.post_builder.set_content("Test content").build()
        
        # Test left alignment
        follower.political_lean = 20
        post.sentiment = Sentiment.LEFT
        follower.interact_with_post(post)
        
        # Test right alignment
        follower.political_lean = 80
        post.sentiment = Sentiment.RIGHT
        follower.interact_with_post(post)
        
        # Test neutral alignment
        follower.political_lean = 50
        post.sentiment = Sentiment.NEUTRAL
        follower.interact_with_post(post)

if __name__ == '__main__':
    unittest.main() 
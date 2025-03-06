import unittest
from unittest.mock import patch, MagicMock
from src.models.post import Post, Sentiment, Comment
from src.factory.post_builder_factory import PostBuilderFactory

class TestPost(unittest.TestCase):
    def setUp(self):
        # Create a post using the factory for each test
        self.post_builder = PostBuilderFactory.get_builder("text")
        self.post = self.post_builder.set_content("Test content").build()

    def test_like_post(self):
        self.post.like()
        self.assertEqual(self.post.likes, 1, "Likes should be incremented to 1")

    def test_unlike_post(self):
        self.post.like()
        self.post.unlike()
        self.assertEqual(self.post.likes, 0, "Likes should be decremented to 0")

    def test_unlike_zero(self):
        # Test unliking a post with 0 likes
        self.post.unlike()
        self.assertEqual(self.post.likes, 0, "Likes should remain at 0")

    def test_share_post(self):
        self.post.share()
        self.assertEqual(self.post.shares, 1, "Shares should be incremented to 1")

    def test_unshare_post(self):
        self.post.share()
        self.post.unshare()
        self.assertEqual(self.post.shares, 0, "Shares should be decremented to 0")

    def test_unshare_zero(self):
        # Test unsharing a post with 0 shares
        self.post.unshare()
        self.assertEqual(self.post.shares, 0, "Shares should remain at 0")
        
    def test_add_comment(self):
        comment = Comment("Great post!", Sentiment.NEUTRAL, "user123")
        self.post.add_comment(comment)
        self.assertEqual(len(self.post.comments), 1, "Comment should be added to post")
        self.assertEqual(self.post.comments[0].content, "Great post!", "Comment content should match")
        
    def test_comment_to_dict(self):
        comment = Comment("Test comment", Sentiment.LEFT, "testuser")
        comment_dict = comment.to_dict()
        self.assertEqual(comment_dict['content'], "Test comment")
        self.assertEqual(comment_dict['sentiment'], "left")
        self.assertEqual(comment_dict['author'], "testuser")
        self.assertTrue('timestamp' in comment_dict)
        
    def test_follower_tracking(self):
        # Test follower gain
        self.post.add_follower_gained()
        self.assertEqual(self.post.followers_gained, 1, "Should track gained follower")
        
        # Test follower loss
        self.post.add_follower_lost()
        self.assertEqual(self.post.followers_lost, 1, "Should track lost follower")
        
    def test_initial_sentiment(self):
        self.post.initial_impressions()  # This will use fallback random sentiment
        self.assertIn(self.post.sentiment, [Sentiment.LEFT, Sentiment.RIGHT, Sentiment.NEUTRAL], 
                     "Post should have valid sentiment")

    @patch('src.models.post.genai')
    def test_analyze_content_left(self, mock_genai):
        # Mock the Google AI response for left sentiment
        mock_response = MagicMock()
        mock_response.text = "left"
        mock_genai.Client.return_value.models.generate_content.return_value = mock_response
        
        result = self.post._analyze_content("Test content")
        self.assertEqual(result, "left")

    @patch('src.models.post.genai')
    def test_analyze_content_invalid(self, mock_genai):
        # Mock an invalid response from Google AI
        mock_response = MagicMock()
        mock_response.text = "invalid"
        mock_genai.Client.return_value.models.generate_content.return_value = mock_response
        
        result = self.post._analyze_content("Test content")
        self.assertEqual(result, "neutral", "Should default to neutral for invalid response")

    def test_initial_impressions_no_api(self):
        with patch('src.models.post.GOOGLE_AI_AVAILABLE', False):
            self.post.initial_impressions()
            self.assertIn(self.post.sentiment, [Sentiment.LEFT, Sentiment.RIGHT, Sentiment.NEUTRAL],
                         "Should fall back to random sentiment when API not available")

    def test_cannot_create_post_directly(self):
        with self.assertRaises(RuntimeError):
            Post("Direct creation should fail")

if __name__ == '__main__':
    unittest.main() 
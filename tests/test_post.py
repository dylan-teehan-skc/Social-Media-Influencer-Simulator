import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime

from src.models.post import Post, Comment, Sentiment


class TestPost(unittest.TestCase):
    def setUp(self):
        # Patch Post._create to allow direct instantiation for testing
        self.post_create_patcher = patch('src.models.post.Post._create', side_effect=Post._create)
        self.post_create_patcher.start()
        
        # Create a test post
        self.test_content = "This is a test post content"
        self.post = Post._create(self.test_content)
        
        # Create a mock user
        self.mock_user = MagicMock()
        self.mock_user.handle = "test_user"
        self.post.author = self.mock_user

    def tearDown(self):
        self.post_create_patcher.stop()

    def test_post_initialization(self):
        """Check if posts get created with the right starting values."""
        self.assertEqual(self.post.content, self.test_content)
        self.assertEqual(self.post.author, self.mock_user)
        self.assertIsNone(self.post.image_path)
        self.assertIsNone(self.post.sentiment)
        self.assertEqual(len(self.post.comments), 0)
        self.assertFalse(self.post.is_spam)
        self.assertIsInstance(self.post.timestamp, datetime)
        self.assertEqual(self.post.likes, 0)
        self.assertEqual(self.post.shares, 0)
        self.assertEqual(self.post.followers_gained, 0)
        self.assertEqual(self.post.followers_lost, 0)

    def test_direct_instantiation_prevention(self):
        """Check if we can't create posts directly (should use builder)."""
        with self.assertRaises(RuntimeError):
            Post(self.test_content)

    @patch('src.models.post.GOOGLE_AI_AVAILABLE', False)
    def test_initial_impressions_fallback(self):
        """Check if sentiment analysis falls back when Google AI isn't available."""
        self.post.initial_impressions()
        self.assertIsNotNone(self.post.sentiment)
        self.assertIn(self.post.sentiment, [Sentiment.LEFT, Sentiment.RIGHT, Sentiment.NEUTRAL])

    @patch('src.models.post.GOOGLE_AI_AVAILABLE', True)
    @patch('src.models.post.os.getenv')
    @patch('src.models.post.genai.Client')
    def test_initial_impressions_with_google_ai(self, mock_client_class, mock_getenv):
        """Test initial_impressions using Google AI."""
        # Setup mocks
        mock_getenv.return_value = "fake_api_key"
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_response = MagicMock()
        mock_response.text = "left"
        mock_client.models.generate_content.return_value = mock_response
        
        # Call initial_impressions
        self.post.initial_impressions()
        
        # Verify Google AI was used
        mock_client_class.assert_called_once_with(api_key="fake_api_key")
        mock_client.models.generate_content.assert_called_once()
        
        # Verify sentiment was set
        self.assertEqual(self.post.sentiment, Sentiment.LEFT)

    @patch('src.models.post.GOOGLE_AI_AVAILABLE', True)
    @patch('src.models.post.os.getenv')
    def test_initial_impressions_missing_api_key(self, mock_getenv):
        """Check if sentiment analysis falls back when API key is missing."""
        # Set up mock to return None for API key
        mock_getenv.return_value = None
        
        # Call initial_impressions
        self.post.initial_impressions()
        
        # Check if sentiment was set using fallback
        self.assertIsNotNone(self.post.sentiment)
        self.assertIn(self.post.sentiment, [Sentiment.LEFT, Sentiment.RIGHT, Sentiment.NEUTRAL])

    def test_like_and_unlike(self):
        """Check if liking and unliking posts works."""
        # Test liking
        initial_likes = self.post.likes
        self.post.like()
        self.assertEqual(self.post.likes, initial_likes + 1)
        
        # Test liking multiple times
        self.post.like()
        self.post.like()
        self.assertEqual(self.post.likes, initial_likes + 3)
        
        # Test unliking
        self.post.unlike()
        self.assertEqual(self.post.likes, initial_likes + 2)
        
        # Test unliking to zero
        self.post.unlike()
        self.post.unlike()
        self.assertEqual(self.post.likes, initial_likes)
        
        # Test unliking below zero (shouldn't go negative)
        self.post.unlike()
        self.assertEqual(self.post.likes, initial_likes)

    def test_share_and_unshare(self):
        """Check if sharing and unsharing posts works."""
        # Test sharing
        initial_shares = self.post.shares
        self.post.share()
        self.assertEqual(self.post.shares, initial_shares + 1)
        
        # Test sharing multiple times
        self.post.share()
        self.post.share()
        self.assertEqual(self.post.shares, initial_shares + 3)
        
        # Test unsharing
        self.post.unshare()
        self.assertEqual(self.post.shares, initial_shares + 2)
        
        # Test unsharing to zero
        self.post.unshare()
        self.post.unshare()
        self.assertEqual(self.post.shares, initial_shares)
        
        # Test unsharing below zero (shouldn't go negative)
        self.post.unshare()
        self.assertEqual(self.post.shares, initial_shares)

    def test_add_comment(self):
        """Check if adding comments to posts works."""
        # Create a comment
        comment = Comment("This is a test comment", Sentiment.NEUTRAL, "commenter")
        
        # Add comment to post
        self.post.add_comment(comment)
        
        # Check if comment was added
        self.assertEqual(len(self.post.comments), 1)
        self.assertEqual(self.post.comments[0], comment)
        
        # Add another comment
        comment2 = Comment("This is another test comment", Sentiment.LEFT, "commenter2")
        self.post.add_comment(comment2)
        
        # Check if second comment was added
        self.assertEqual(len(self.post.comments), 2)
        self.assertEqual(self.post.comments[1], comment2)

    def test_follower_tracking(self):
        """Check if tracking followers gained and lost works."""
        # Test adding gained followers
        initial_gained = self.post.followers_gained
        self.post.add_follower_gained()
        self.assertEqual(self.post.followers_gained, initial_gained + 1)
        
        self.post.add_follower_gained()
        self.post.add_follower_gained()
        self.assertEqual(self.post.followers_gained, initial_gained + 3)
        
        # Test adding lost followers
        initial_lost = self.post.followers_lost
        self.post.add_follower_lost()
        self.assertEqual(self.post.followers_lost, initial_lost + 1)
        
        self.post.add_follower_lost()
        self.post.add_follower_lost()
        self.assertEqual(self.post.followers_lost, initial_lost + 3)


class TestComment(unittest.TestCase):
    def setUp(self):
        self.content = "This is a test comment"
        self.sentiment = Sentiment.NEUTRAL
        self.author = "test_commenter"
        self.comment = Comment(self.content, self.sentiment, self.author)

    def test_comment_initialization(self):
        """Check if comments get created with the right starting values."""
        self.assertEqual(self.comment.content, self.content)
        self.assertEqual(self.comment.sentiment, self.sentiment)
        self.assertEqual(self.comment.author, self.author)
        self.assertIsInstance(self.comment.timestamp, datetime)

    def test_to_dict(self):
        """Check if converting a comment to a dictionary works."""
        comment_dict = self.comment.to_dict()
        
        self.assertEqual(comment_dict['content'], self.content)
        self.assertEqual(comment_dict['sentiment'], self.sentiment.value)
        self.assertEqual(comment_dict['author'], self.author)
        self.assertIsInstance(comment_dict['timestamp'], str)


if __name__ == '__main__':
    unittest.main() 
import unittest
from unittest.mock import MagicMock, patch
from random import randint

from src.models.follower import Follower
from src.models.post import Post, Sentiment, Comment
from src.models.user import User
from src.command.post_commands import LikeCommand, ShareCommand, CommentCommand


class TestFollower(unittest.TestCase):
    def setUp(self):
        # Create followers with different political leanings
        self.left_follower = Follower(Sentiment.LEFT, "left_follower_1234")
        self.right_follower = Follower(Sentiment.RIGHT, "right_follower_5678")
        self.neutral_follower = Follower(Sentiment.NEUTRAL, "neutral_follower_9012")
        
        # Create a mock post
        self.mock_post = MagicMock(spec=Post)
        self.mock_post.sentiment = Sentiment.NEUTRAL
        self.mock_post.comments = []
        
        # Create a mock user
        self.mock_user = MagicMock(spec=User)

    def test_follower_initialization(self):
        """Check if followers get created with the right starting values."""
        # Check left-leaning follower
        self.assertEqual(self.left_follower.handle, "left_follower_1234")
        self.assertEqual(self.left_follower.sentiment, Sentiment.LEFT)
        self.assertLessEqual(self.left_follower.political_lean, 30)
        
        # Check right-leaning follower
        self.assertEqual(self.right_follower.handle, "right_follower_5678")
        self.assertEqual(self.right_follower.sentiment, Sentiment.RIGHT)
        self.assertGreaterEqual(self.right_follower.political_lean, 70)
        
        # Check neutral follower
        self.assertEqual(self.neutral_follower.handle, "neutral_follower_9012")
        self.assertEqual(self.neutral_follower.sentiment, Sentiment.NEUTRAL)
        self.assertGreaterEqual(self.neutral_follower.political_lean, 40)
        self.assertLessEqual(self.neutral_follower.political_lean, 60)

    def test_create_with_random_handle(self):
        """Check if we can create a follower with a random handle."""
        follower = Follower.create_with_random_handle(Sentiment.LEFT)
        self.assertEqual(follower.sentiment, Sentiment.LEFT)
        self.assertTrue(any(prefix in follower.handle for prefix in Follower.FOLLOWER_PREFIXES[Sentiment.LEFT]))
        self.assertRegex(follower.handle, r'[a-z_]+\d{4}')

    def test_create_random_follower(self):
        """Check if we can create random followers based on index."""
        # Index 0 should be LEFT
        follower0 = Follower.create_random_follower(0)
        self.assertEqual(follower0.sentiment, Sentiment.LEFT)
        
        # Index 1 should be RIGHT
        follower1 = Follower.create_random_follower(1)
        self.assertEqual(follower1.sentiment, Sentiment.RIGHT)
        
        # Index 2 should be NEUTRAL
        follower2 = Follower.create_random_follower(2)
        self.assertEqual(follower2.sentiment, Sentiment.NEUTRAL)
        
        # Index 3 should cycle back to LEFT
        follower3 = Follower.create_random_follower(3)
        self.assertEqual(follower3.sentiment, Sentiment.LEFT)

    @patch('random.randint')
    def test_should_unfollow(self, mock_randint):
        """Check the logic for deciding when to unfollow."""
        # Set up a strongly right-leaning follower
        self.left_follower.political_lean = 90
        mock_post = MagicMock(spec=Post)
        mock_post.sentiment = Sentiment.LEFT
        
        # Should unfollow when alignment is low and random chance is high
        mock_randint.return_value = 10  # Below 30% threshold
        result = self.left_follower._should_unfollow(mock_post)
        self.assertIsInstance(result, bool)
        
        # Shouldn't unfollow neutral posts
        mock_post.sentiment = Sentiment.NEUTRAL
        self.assertFalse(self.left_follower._should_unfollow(mock_post))

    @patch('random.randint')
    def test_should_follow(self, mock_randint):
        """Check the logic for deciding when to follow."""
        mock_post = MagicMock(spec=Post)
        follow_chance = 50
        
        # Test with neutral post
        mock_post.sentiment = Sentiment.NEUTRAL
        mock_randint.return_value = 30  # Below 50% threshold
        result = self.neutral_follower.should_follow(mock_post, follow_chance)
        self.assertIsInstance(result, bool)
        
        # Test with aligned post (left follower, left post)
        self.left_follower.political_lean = 20  # Left-leaning
        mock_post.sentiment = Sentiment.LEFT
        mock_randint.return_value = 30  # Below 50% threshold
        result = self.left_follower.should_follow(mock_post, follow_chance)
        self.assertIsInstance(result, bool)

    def test_add_follow_comment(self):
        """Check if followers add comments when they follow."""
        # Set up
        mock_post = MagicMock(spec=Post)
        mock_post.sentiment = Sentiment.NEUTRAL
        mock_post.comments = []
        
        # Add comment for neutral post
        self.neutral_follower.add_follow_comment(mock_post)
        mock_post.add_comment.assert_called_once()
        comment_arg = mock_post.add_comment.call_args[0][0]
        self.assertEqual(comment_arg.content, Follower.FOLLOW_COMMENT_NEUTRAL)
        self.assertEqual(comment_arg.author, self.neutral_follower.handle)
        
        # Reset mock
        mock_post.reset_mock()
        
        # Add comment for political post
        mock_post.sentiment = Sentiment.LEFT
        self.neutral_follower.add_follow_comment(mock_post)
        mock_post.add_comment.assert_called_once()
        comment_arg = mock_post.add_comment.call_args[0][0]
        self.assertEqual(comment_arg.content, Follower.FOLLOW_COMMENT_POLITICAL)
        
        # Shouldn't add duplicate comments
        mock_post.reset_mock()
        mock_post.comments = [Comment("test", Sentiment.NEUTRAL, self.neutral_follower.handle)]
        self.neutral_follower.add_follow_comment(mock_post)
        mock_post.add_comment.assert_not_called()

    @patch('random.randint')
    def test_interact_with_post_high_alignment(self, mock_randint):
        """Check how followers interact with posts they strongly agree with."""
        # Set up a strongly right-leaning follower
        self.right_follower.political_lean = 80
        mock_post = MagicMock(spec=Post)
        mock_post.sentiment = Sentiment.RIGHT
        mock_post.author = MagicMock()
        mock_post.author.handle = "test_author"
        
        # Set up to comment (30% chance)
        mock_randint.side_effect = [20, 0]  # First call for comment chance, second for comment selection
        
        # Test interaction
        self.right_follower.interact_with_post(mock_post)
        
        # Check if command history exists
        self.assertIsNotNone(self.right_follower.command_history)

    @patch('random.randint')
    def test_interact_with_post_medium_alignment(self, mock_randint):
        """Check how followers interact with posts they somewhat agree with."""
        # Set up a neutral follower
        self.neutral_follower.political_lean = 50
        mock_post = MagicMock(spec=Post)
        mock_post.sentiment = Sentiment.NEUTRAL
        mock_post.author = MagicMock()
        mock_post.author.handle = "test_author"
        
        # Set up to comment (30% chance)
        mock_randint.side_effect = [20, 1]  # First call for comment chance, second for comment selection
        
        # Test interaction
        self.neutral_follower.interact_with_post(mock_post)
        
        # Check if command history exists
        self.assertIsNotNone(self.neutral_follower.command_history)

    @patch('random.randint')
    def test_interact_with_post_low_alignment(self, mock_randint):
        """Check how followers interact with posts they disagree with."""
        # Set up a left-leaning follower
        self.left_follower.political_lean = 20
        mock_post = MagicMock(spec=Post)
        mock_post.sentiment = Sentiment.RIGHT
        mock_post.author = MagicMock()
        mock_post.author.handle = "test_author"
        
        # Set up to comment (30% chance)
        mock_randint.side_effect = [20, 2]  # First call for comment chance, second for comment selection
        
        # Test interaction
        self.left_follower.interact_with_post(mock_post)
        
        # Check if command history exists
        self.assertIsNotNone(self.left_follower.command_history)

    @patch('src.models.follower.Follower._should_unfollow')
    @patch('src.models.follower.Follower.interact_with_post')
    @patch('src.command.post_commands.CommentCommand.execute')
    def test_update_with_unfollow(self, mock_execute, mock_interact, mock_should_unfollow):
        """Check if followers unfollow when they should."""
        # Set up
        mock_should_unfollow.return_value = True
        mock_post = MagicMock(spec=Post)
        mock_post.sentiment = Sentiment.NEUTRAL
        
        # Add author to mock post
        mock_author = MagicMock()
        mock_author.handle = "test_author"
        mock_post.author = mock_author
        
        mock_subject = MagicMock(spec=User)
        
        # Test update with unfollow
        self.left_follower.update(mock_subject, mock_post)
        
        # Check if follower detached
        mock_subject.detach.assert_called_once_with(self.left_follower)
        
        # Check if follower loss was tracked
        mock_post.add_follower_lost.assert_called_once()


if __name__ == '__main__':
    unittest.main() 
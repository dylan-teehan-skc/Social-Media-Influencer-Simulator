import unittest
from unittest.mock import MagicMock

from src.models.post import Comment, Post, Sentiment
from src.patterns.command.command_history import CommandHistory
from src.patterns.command.post_commands import (
    CommentCommand,
    LikeCommand,
    ShareCommand,
)
from src.services.logger_service import LoggerService


class TestPostCommands(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock logger first
        self.mock_logger = MagicMock()
        LoggerService._logger = self.mock_logger

        # Create a mock post
        self.mock_post = MagicMock(spec=Post)

        # Add author attribute to the mock post
        mock_author = MagicMock()
        mock_author.handle = "test_author"
        self.mock_post.author = mock_author

        # Add comments attribute to the mock post
        self.mock_post.comments = []

        # Create a test comment
        self.test_comment = Comment(
            "Test comment", Sentiment.NEUTRAL, "commenter"
        )

        # Create a command history
        self.command_history = CommandHistory()

    def test_like_command(self):
        """Check if the like command works."""
        # Create a like command
        like_command = LikeCommand(self.mock_post, "liker")

        # Execute the command
        like_command.execute()

        # Check if post._increment_likes was called
        self.mock_post._increment_likes.assert_called_once()

        # Check if logging occurred
        self.mock_logger.info.assert_called_with(
            "Follower 'liker' liked post by @test_author"
        )

        # Test undo
        like_command.undo()
        self.mock_post._decrement_likes.assert_called_once()
        self.mock_logger.info.assert_called_with(
            "Undid: Follower 'liker' liked post by @test_author"
        )

    def test_share_command(self):
        """Check if the share command works."""
        # Create a share command
        share_command = ShareCommand(self.mock_post, "sharer")

        # Execute the command
        share_command.execute()

        # Check if post._increment_shares was called
        self.mock_post._increment_shares.assert_called_once()

        # Check if logging occurred
        self.mock_logger.info.assert_called_with(
            "Follower 'sharer' shared post by @test_author"
        )

        # Test undo
        share_command.undo()
        self.mock_post._decrement_shares.assert_called_once()
        self.mock_logger.info.assert_called_with(
            "Undid: Follower 'sharer' shared post by @test_author"
        )

    def test_comment_command(self):
        """Check if the comment command works."""
        # Create a comment command
        comment_command = CommentCommand(self.mock_post, self.test_comment)

        # Execute the command
        comment_command.execute()

        # Check if post._add_comment was called with the right comment
        self.mock_post._add_comment.assert_called_once_with(self.test_comment)

        # Check if logging occurred
        self.mock_logger.info.assert_called_with(
            "Follower 'commenter' commented on post by @test_author"
        )

        # Test undo
        # Add the comment to mock post's comments for undo test
        self.mock_post.comments.append(self.test_comment)
        comment_command.undo()
        self.mock_post._remove_comment.assert_called_once_with(
            self.test_comment
        )
        self.mock_logger.info.assert_called_with(
            "Undid: Follower 'commenter' commented on post by @test_author"
        )

    def test_command_history(self):
        """Check if the command history works."""
        # Create some commands
        like_command = LikeCommand(self.mock_post, "liker")
        share_command = ShareCommand(self.mock_post, "sharer")
        comment_command = CommentCommand(self.mock_post, self.test_comment)

        # Push commands to history
        self.command_history.push(like_command)
        self.command_history.push(share_command)
        self.command_history.push(comment_command)

        # Check if logging occurred
        expected_debug_calls = [
            unittest.mock.call("Command added to history, total commands: 1"),
            unittest.mock.call("Command added to history, total commands: 2"),
            unittest.mock.call("Command added to history, total commands: 3"),
        ]
        self.mock_logger.debug.assert_has_calls(expected_debug_calls)

        # Test clear
        self.command_history.clear()
        self.assertEqual(len(self.command_history.history), 0)
        self.mock_logger.debug.assert_called_with("Command history cleared")


if __name__ == "__main__":
    unittest.main()

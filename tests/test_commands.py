import unittest
from unittest.mock import MagicMock
from src.command.post_commands import LikeCommand, CommentCommand, ShareCommand, CommandHistory
from src.models.post import Post, Comment, Sentiment
from src.factory.post_builder_factory import PostBuilderFactory

class TestCommands(unittest.TestCase):
    def setUp(self):
        self.post_builder = PostBuilderFactory.get_builder("text")
        self.post = self.post_builder.set_content("Test content").build()
        self.post.author = MagicMock(handle="test_author")
        self.command_history = CommandHistory()

    def test_like_command(self):
        # Test like command execution
        like_command = LikeCommand(self.post, "test_user")
        like_command.execute()
        self.assertEqual(self.post.likes, 1)

        # Test command history
        self.command_history.push(like_command)
        self.assertEqual(len(self.command_history.history), 1)

    def test_comment_command(self):
        # Test comment command execution
        comment = Comment("Test comment", Sentiment.NEUTRAL, "test_user")
        comment_command = CommentCommand(self.post, comment)
        comment_command.execute()
        self.assertEqual(len(self.post.comments), 1)
        self.assertEqual(self.post.comments[0].content, "Test comment")

        # Test comment undo
        comment_command.undo()
        self.assertEqual(len(self.post.comments), 0)

    def test_share_command(self):
        # Test share command execution
        share_command = ShareCommand(self.post, "test_user")
        share_command.execute()
        self.assertEqual(self.post.shares, 1)

        # Test share undo
        share_command.undo()
        self.assertEqual(self.post.shares, 0)

    def test_command_history_clear(self):
        # Add multiple commands to history
        like_command = LikeCommand(self.post, "test_user")
        share_command = ShareCommand(self.post, "test_user")
        
        self.command_history.push(like_command)
        self.command_history.push(share_command)
        self.assertEqual(len(self.command_history.history), 2)

        # Test clear functionality
        self.command_history.clear()
        self.assertEqual(len(self.command_history.history), 0)

if __name__ == '__main__':
    unittest.main() 
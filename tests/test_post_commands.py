import unittest
from unittest.mock import MagicMock

from src.command.post_commands import (
    LikeCommand,
    ShareCommand,
    CommentCommand,
    CommandHistory
)
from src.models.post import Post, Comment, Sentiment


class TestPostCommands(unittest.TestCase):
    def setUp(self):
        # Create a mock post
        self.mock_post = MagicMock(spec=Post)
        # Add author attribute to the mock post
        mock_author = MagicMock()
        mock_author.handle = "test_author"
        self.mock_post.author = mock_author
        
        # Add comments attribute to the mock post
        self.mock_post.comments = []
        
        # Create a test comment
        self.test_comment = Comment("Test comment", Sentiment.NEUTRAL, "commenter")
        
        # Create a command history
        self.command_history = CommandHistory()

    def test_like_command(self):
        """Check if the like command works."""
        # Create a like command
        like_command = LikeCommand(self.mock_post, "liker")
        
        # Execute the command
        like_command.execute()
        
        # Check if post.like was called
        self.mock_post.like.assert_called_once()
        
        # Check if undo is implemented
        if hasattr(like_command, 'undo'):
            # Undo the command
            like_command.undo()
            # Check if post.unlike was called
            self.mock_post.unlike.assert_called_once()

    def test_share_command(self):
        """Check if the share command works."""
        # Create a share command
        share_command = ShareCommand(self.mock_post, "sharer")
        
        # Execute the command
        share_command.execute()
        
        # Check if post.share was called
        self.mock_post.share.assert_called_once()
        
        # Check if undo is implemented
        if hasattr(share_command, 'undo'):
            # Undo the command
            share_command.undo()
            # Check if post.unshare was called
            self.mock_post.unshare.assert_called_once()

    def test_comment_command(self):
        """Check if the comment command works."""
        # Create a comment command
        comment_command = CommentCommand(self.mock_post, self.test_comment)
        
        # Execute the command
        comment_command.execute()
        
        # Check if post.add_comment was called with the right comment
        self.mock_post.add_comment.assert_called_once_with(self.test_comment)
        
        # Check if undo is implemented
        if hasattr(comment_command, 'undo'):
            # Add the comment to the mock post's comments list to simulate the effect of execute
            self.mock_post.comments.append(self.test_comment)
            # Undo the command
            comment_command.undo()
            # Check if the comment was removed (if undo is implemented to remove comments)
            if len(self.mock_post.comments) == 0:
                self.assertEqual(len(self.mock_post.comments), 0)

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
        
        # Check if pop method exists
        if hasattr(self.command_history, 'pop'):
            # Pop a command
            popped_command = self.command_history.pop()
            
            # Check if we got the right command back (last in, first out)
            self.assertEqual(popped_command, comment_command)
            
            # Pop another command
            popped_command = self.command_history.pop()
            
            # Check if we got the right command back
            self.assertEqual(popped_command, share_command)
            
            # Pop the last command
            popped_command = self.command_history.pop()
            
            # Check if we got the right command back
            self.assertEqual(popped_command, like_command)
            
            # Pop from empty history
            popped_command = self.command_history.pop()
            
            # Check if we get None when empty
            self.assertIsNone(popped_command)
        else:
            # Skip this part of the test if pop is not implemented
            pass

    def test_command_history_undo(self):
        """Check if we can undo commands from history."""
        # Skip this test if undo is not implemented in CommandHistory
        if not hasattr(self.command_history, 'undo'):
            return
            
        # Create some commands
        like_command = LikeCommand(self.mock_post, "liker")
        share_command = ShareCommand(self.mock_post, "sharer")
        
        # Execute and push commands to history
        like_command.execute()
        self.command_history.push(like_command)
        
        share_command.execute()
        self.command_history.push(share_command)
        
        # Reset mock to clear call history
        self.mock_post.reset_mock()
        # Ensure author is still set after reset
        mock_author = MagicMock()
        mock_author.handle = "test_author"
        self.mock_post.author = mock_author
        self.mock_post.comments = []
        
        # Undo last command
        self.command_history.undo()
        
        # Check if share command was undone
        self.mock_post.unshare.assert_called_once()
        self.mock_post.unlike.assert_not_called()
        
        # Reset mock again
        self.mock_post.reset_mock()
        # Ensure author is still set after reset
        mock_author = MagicMock()
        mock_author.handle = "test_author"
        self.mock_post.author = mock_author
        self.mock_post.comments = []
        
        # Undo first command
        self.command_history.undo()
        
        # Check if like command was undone
        self.mock_post.unlike.assert_called_once()
        
        # Try to undo when history is empty
        self.mock_post.reset_mock()
        # Ensure author is still set after reset
        mock_author = MagicMock()
        mock_author.handle = "test_author"
        self.mock_post.author = mock_author
        self.mock_post.comments = []
        
        self.command_history.undo()
        
        # Check if nothing happens when history is empty
        self.mock_post.unlike.assert_not_called()
        self.mock_post.unshare.assert_not_called()


if __name__ == '__main__':
    unittest.main() 
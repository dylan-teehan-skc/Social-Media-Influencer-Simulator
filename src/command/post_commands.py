from src.interfaces.command import Command
from src.models.post import Post, Comment
from src.services.logger_service import LoggerService
from typing import Optional

class LikeCommand(Command):
    """Command for liking a post."""
    
    def __init__(self, post: Post, follower_handle: str):
        self.post = post
        self.follower_handle = follower_handle
        self.logger = LoggerService.get_logger()
        
    def execute(self) -> None:
        self.post.like()
        self.logger.info(f"Follower '{self.follower_handle}' liked post by @{self.post.author.handle}")


class CommentCommand(Command):
    """Command for commenting on a post."""
    
    def __init__(self, post: Post, comment: Comment):
        self.post = post
        self.comment = comment
        self.logger = LoggerService.get_logger()
        
    def execute(self) -> None:
        self.post.add_comment(self.comment)
        self.logger.info(f"Follower '{self.comment.author}' commented on post by @{self.post.author.handle}: '{self.comment.content[:30]}...' if len(self.comment.content) > 30 else self.comment.content")


class ShareCommand(Command):
    """Command for sharing a post."""
    
    def __init__(self, post: Post, follower_handle: str):
        self.post = post
        self.follower_handle = follower_handle
        self.logger = LoggerService.get_logger()
        
    def execute(self) -> None:
        self.post.share()
        self.logger.info(f"Follower '{self.follower_handle}' shared post by @{self.post.author.handle}")


class CommandHistory:

    def __init__(self):
        self.history = []
        self.logger = LoggerService.get_logger()
        
    def push(self, command: Command) -> None:
        """Add a command to the history after execution."""
        self.history.append(command)
        self.logger.debug(f"Command added to history, total commands: {len(self.history)}")
        
    def clear(self) -> None:
        """Clear the command history."""
        self.history.clear()
        self.logger.debug("Command history cleared") 
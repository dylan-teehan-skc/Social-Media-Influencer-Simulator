from src.interfaces.command import Command
from src.models.post import Comment, Post
from src.services.logger_service import LoggerService


class LikeCommand(Command):
    """Command for liking a post."""

    def __init__(self, post: Post, follower_handle: str):
        self.post = post
        self.follower_handle = follower_handle
        self.logger = LoggerService.get_logger()

    def execute(self) -> None:
        self.post.like()
        author_info = f"@{self.post.author.handle}" if self.post.author else "(no author)"
        self.logger.info(f"Follower '{self.follower_handle}' liked post by {author_info}")


class CommentCommand(Command):
    """Command for commenting on a post."""

    def __init__(self, post: Post, comment: Comment):
        self.post = post
        self.comment = comment
        self.logger = LoggerService.get_logger()

    def execute(self) -> None:
        self.post.add_comment(self.comment)
        author_info = f"@{self.post.author.handle}" if self.post.author else "(no author)"
        self.logger.info(f"Follower '{self.comment.author}' commented on post by {author_info}")

    def undo(self) -> None:
        if self.comment in self.post.comments:
            self.post.comments.remove(self.comment)
            author_info = f"@{self.post.author.handle}" if self.post.author else "(no author)"
            self.logger.info(f"Undid: Follower '{self.comment.author}' commented on post by {author_info}")


class ShareCommand(Command):
    """Command for sharing a post."""

    def __init__(self, post: Post, follower_handle: str):
        self.post = post
        self.follower_handle = follower_handle
        self.logger = LoggerService.get_logger()

    def execute(self) -> None:
        self.post.share()
        author_info = f"@{self.post.author.handle}" if self.post.author else "(no author)"
        self.logger.info(f"Follower '{self.follower_handle}' shared post by {author_info}")

    def undo(self) -> None:
        self.post.unshare()
        author_info = f"@{self.post.author.handle}" if self.post.author else "(no author)"
        self.logger.info(f"Undid: Follower '{self.follower_handle}' shared post by {author_info}")


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

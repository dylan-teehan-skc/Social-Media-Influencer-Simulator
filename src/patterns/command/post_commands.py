from src.models.post import Comment, Post
from src.patterns.interfaces.command import Command
from src.services.logger_service import LoggerService


class LikeCommand(Command):
    # Command for liking a post

    def __init__(self, post: Post, follower_handle: str):
        self.post = post
        self.follower_handle = follower_handle
        self.logger = LoggerService.get_logger()

    def execute(self) -> None:
        # Increment post likes and log the action
        self.post._increment_likes()
        author_info = (
            f"@{self.post.author.handle}"
            if self.post.author
            else "(no author)"
        )
        self.logger.info(
            f"Follower '{self.follower_handle}' liked post by {author_info}"
        )

    def undo(self) -> None:
        # Decrement post likes and log the undo action
        self.post._decrement_likes()
        author_info = (
            f"@{self.post.author.handle}"
            if self.post.author
            else "(no author)"
        )
        self.logger.info(
            f"Undid: Follower '{self.follower_handle}' liked post by {author_info}"
        )


class CommentCommand(Command):
    # Command to add a comment to a post

    def __init__(self, post: Post, comment: Comment):
        # Initialize with post and comment
        self.post = post
        self.comment = comment
        self.logger = LoggerService.get_logger()

    def execute(self) -> None:
        # Add comment to post and log the action
        self.post._add_comment(self.comment)
        author_info = (
            f"@{self.post.author.handle}"
            if self.post.author
            else "(no author)"
        )
        self.logger.info(
            f"Follower '{self.comment.author}' commented on post by {author_info}"
        )

    def undo(self) -> None:
        # Remove comment from post and log the undo action
        if self.comment in self.post.comments:
            self.post._remove_comment(self.comment)
            author_info = (
                f"@{self.post.author.handle}"
                if self.post.author
                else "(no author)"
            )
            self.logger.info(
                f"Undid: Follower '{self.comment.author}' commented on post by {author_info}"
            )


class ShareCommand(Command):
    # Command for sharing a post

    def __init__(self, post: Post, follower_handle: str):
        self.post = post
        self.follower_handle = follower_handle
        self.logger = LoggerService.get_logger()

    def execute(self) -> None:
        # Increment post shares and log the action
        self.post._increment_shares()
        author_info = (
            f"@{self.post.author.handle}"
            if self.post.author
            else "(no author)"
        )
        self.logger.info(
            f"Follower '{self.follower_handle}' shared post by {author_info}"
        )

    def undo(self) -> None:
        # Decrement post shares and log the undo action
        self.post._decrement_shares()
        author_info = (
            f"@{self.post.author.handle}"
            if self.post.author
            else "(no author)"
        )
        self.logger.info(
            f"Undid: Follower '{self.follower_handle}' shared post by {author_info}"
        )

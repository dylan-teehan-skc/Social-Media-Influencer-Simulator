from .post_command import PostCommand
from ..models.post import Post, Comment
from .follower_protocol import FollowerProtocol

class CommentCommand(PostCommand):
    def __init__(self, post: Post, follower: FollowerProtocol, comment_text: str):
        super().__init__()
        self.post = post
        self.follower = follower
        self.comment_text = comment_text
        self.comment = None
        
    def execute(self) -> None:
        self.comment = Comment(self.comment_text, self.follower.sentiment, self.follower.handle)
        self.post.comments.append(self.comment)
        self.logger.debug("Follower %s commented on post by %s: %s", 
                         self.follower.handle, self.post.author.handle, self.comment_text)
            
    def undo(self) -> None:
        if self.comment and self.comment in self.post.comments:
            self.post.comments.remove(self.comment)
            self.logger.debug("Removed comment from %s on post by %s", 
                            self.follower.handle, self.post.author.handle)
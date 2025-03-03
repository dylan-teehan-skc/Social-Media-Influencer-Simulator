from .post_command import PostCommand
from ..models.post import Post
from .follower_protocol import FollowerProtocol

class ShareCommand(PostCommand):
    def __init__(self, post: Post, follower: FollowerProtocol):
        super().__init__()
        self.post = post
        self.follower = follower
        
    def execute(self) -> None:
        if self.follower.handle not in self.post.shared_by:
            self.post.shares += 1
            self.post.shared_by.add(self.follower.handle)
            self.logger.debug("Follower %s shared post by %s", 
                            self.follower.handle, self.post.author.handle)
            
    def undo(self) -> None:
        if self.follower.handle in self.post.shared_by:
            self.post.shares -= 1
            self.post.shared_by.remove(self.follower.handle)
            self.logger.debug("Follower %s unshared post by %s", 
                            self.follower.handle, self.post.author.handle) 
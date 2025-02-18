from datetime import datetime
from typing import List
from enum import Enum
from .follower import Follower, Comment

class Sentiment(Enum):
    LEFT = "left"
    RIGHT = "right"
    NEUTRAL = "neutral"

class Post:
    def __init__(self, content: str):
        self.content: str = content
        self.timestamp: datetime = datetime.now()
        self.likes: List[Follower] = []
        self.shares: List[Follower] = []
        self.sentiment: Sentiment = Sentiment.NEUTRAL
        self.comments: List[Comment] = []
    
    def initial_impressions(self) -> None:
        # TODO: Implement initial impressions
        # analyse post content and set sentiment
        # user reactions will depend on sentiment
        pass

    def like(self, follower: Follower) -> None:
        self.likes.append(follower)
        
    def unlike(self, follower: Follower) -> None:
        self.likes.remove(follower)

    def share(self, follower: Follower) -> None:
        self.shares.append(follower)

    def unshare(self, follower: Follower) -> None:
        self.shares.remove(follower)

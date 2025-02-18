from datetime import datetime
from typing import List
from enum import Enum

class Sentiment(Enum):
    LEFT = "left"
    RIGHT = "right"
    NEUTRAL = "neutral"

class Post:
    def __init__(self, content: str):
        self.content: str = content
        self.timestamp: datetime = datetime.now()
        self.likes: int = 0
        self.shares: int = 0
        self.sentiment: Sentiment = Sentiment.NEUTRAL
        self.comments: List[Comment] = []
    
    def initial_impressions(self) -> None:
        # TODO: Implement initial impressions
        # analyse post content and set sentiment
        # user reactions will depend on sentiment
        pass

    def like(self, follower: Follower) -> None:
        self.likes += 1
        
    def unlike(self) -> None:
        self.likes -= 1

    def share(self, follower: Follower) -> None:
        self.shares += 1

    def unshare(self) -> None:
        self.shares -= 1

class Comment:
    def __init__(self, content: str, sentiment: Sentiment, authorhandle: str):
        self.content: str = content
        self.sentiment: Sentiment = sentiment
        self.timestamp: datetime = datetime.now()
        self.author: str = authorhandle

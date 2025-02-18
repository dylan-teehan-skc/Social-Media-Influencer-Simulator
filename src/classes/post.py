from datetime import datetime
from typing import List

class Post:
    def __init__(self, content: str):
        self.content: str = content
        self.timestamp: datetime = datetime.now()
        self.likes: int = 0
        self.shares: int = 0

    def like(self) -> None:
        self.likes += 1
        
    def unlike(self) -> None:
        if self.likes > 0:
            self.likes -= 1

    def share(self) -> None:
        self.shares += 1

    def unshare(self) -> None:
        if self.shares > 0:
            self.shares -= 1

from typing import List
from random import randint
from .post import Post, Sentiment, Comment
from datetime import datetime
from ..interfaces.observer import Observer  

class Follower(Observer):  
    def __init__(self, sentiment: Sentiment, handle: str):
        self.handle = handle  
        
        # Set initial political lean based on sentiment
        if sentiment == Sentiment.LEFT:
            self.political_lean = randint(0, 30)  # Left-leaning: 0-30
        elif sentiment == Sentiment.RIGHT:
            self.political_lean = randint(70, 100)  # Right-leaning: 70-100
        else:
            self.political_lean = randint(40, 60)  # Neutral: 40-60
        
        self.sentiment = sentiment  # Store the follower's sentiment
        
        self.positive_comments = [
            "Couldn't agree more!",
            "This is exactly what I've been saying!",
            "Great point!",
            "Thanks for sharing this important message!",
            "Absolutely spot on!"
        ]
        
        self.neutral_comments = [
            "Interesting perspective.",
            "Something to think about.",
            "I see your point.",
            "Worth considering.",
            "Thanks for sharing."
        ]
        
        self.negative_comments = [
            "I respectfully disagree.",
            "Not sure I can agree with this.",
            "You might want to reconsider this.",
            "I see it differently.",
            "Let's agree to disagree."
        ]

    def update(self, subject, post=None):
        if post:
            self.interact_with_post(post)
            
            # Chance to unfollow if strongly disagree with post
            if self._should_unfollow(post):
                subject.detach(self)
                post.add_comment(Comment("I can't support this content. Unfollowing.", self.sentiment, self.handle))
                post.add_follower_lost()  # Track lost follower

    def _should_unfollow(self, post: Post) -> bool:
        if post.sentiment == Sentiment.LEFT:
            alignment = 100 - self.political_lean
        elif post.sentiment == Sentiment.RIGHT:
            alignment = self.political_lean
        else:
            return False  # Don't unfollow for neutral posts
            
        # Higher chance to unfollow if strongly opposed to the post's sentiment
        return alignment < 20 and randint(1, 100) <= 30  # 30% chance if alignment < 20

    def _get_comment(self, alignment: float) -> str:
        if alignment > 70:
            return self.positive_comments[randint(0, len(self.positive_comments) - 1)]
        elif alignment > 40:
            return self.neutral_comments[randint(0, len(self.neutral_comments) - 1)]
        else:
            return self.negative_comments[randint(0, len(self.negative_comments) - 1)]

    def _adjust_lean_from_sentiment(self, sentiment: Sentiment) -> None:
        if sentiment == Sentiment.RIGHT:
            adjustment = randint(0, 10)
            self.political_lean = min(100, self.political_lean + adjustment)
        elif sentiment == Sentiment.LEFT:
            adjustment = randint(0, 10)
            self.political_lean = max(0, self.political_lean - adjustment)

    def interact_with_post(self, post: Post) -> None:
        self._adjust_lean_from_sentiment(post.sentiment)

        if post.sentiment == Sentiment.LEFT:
            alignment = 100 - self.political_lean
        elif post.sentiment == Sentiment.RIGHT:
            alignment = self.political_lean
        else:
            alignment = 100 - abs(50 - self.political_lean) * 2

        if randint(1, 100) <= 30:
            comment = self._get_comment(alignment)
            post.add_comment(Comment(comment, self.sentiment, self.handle))

        if alignment > 70:
            post.like(self)
            post.share(self)
        elif alignment > 40:
            post.like(self)

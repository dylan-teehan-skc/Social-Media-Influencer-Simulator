from typing import List
from random import randint
from .post import Post, Sentiment, Comment
from datetime import datetime
from observer.observer import Observer  

class Follower(Observer):  
    def __init__(self, sentiment: Sentiment, handle: str):
        self.handle = handle  
        self.political_lean = 50  
        
        # Initial sentiment adjustment
        initial_sentiment = sentiment 
        self._adjust_lean_from_sentiment(initial_sentiment)
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
            print(f"{self.handle} received a new post from {subject.handle}: {post.content}")
            self.interact_with_post(post) 

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
            post.add_comment(Comment(comment, post.sentiment, self.handle))

        if alignment > 70:
            post.like(self)
            post.share(self)
        elif alignment > 40:
            post.like(self)

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from PyQt6.QtCore import QObject, pyqtSignal

from src.services.logger_service import LoggerService

if TYPE_CHECKING:
    pass

try:
    from google import genai
    from google.api_core import exceptions as google_exceptions

    GOOGLE_AI_AVAILABLE = True
except ImportError:
    GOOGLE_AI_AVAILABLE = False


class Sentiment(Enum):
    LEFT = "left"
    RIGHT = "right"
    NEUTRAL = "neutral"


class Comment(QObject):
    # Comment model representing a comment on a post

    def __init__(self, content, sentiment, author):
        super().__init__()
        self._content = content
        self._sentiment = sentiment
        self._author = author
        self._timestamp = datetime.now()

    @property
    def content(self):
        return self._content

    @property
    def sentiment(self):
        return self._sentiment

    @property
    def author(self):
        return self._author

    @property
    def timestamp(self):
        return self._timestamp

    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "sentiment": self.sentiment.value,
            "timestamp": self.timestamp.isoformat(),
            "author": self.author,
        }


# pylint: disable=R0902
class Post(QObject):
    # Post model representing a social media post with engagement metrics

    # Signals for UI updates
    likes_changed = pyqtSignal(int)
    shares_changed = pyqtSignal(int)
    comments_changed = pyqtSignal(list)
    sentiment_changed = pyqtSignal(object)
    followers_gained_changed = pyqtSignal(int)
    followers_lost_changed = pyqtSignal(int)

    def __init__(self, content, author=None, image_path=None):
        # Initialize a post with content, author, and optional image
        super().__init__()
        self._content = content
        self._author = author
        self._image_path = image_path
        self._likes = 0
        self._shares = 0
        self._comments = []
        self._timestamp = datetime.now()
        self._sentiment = Sentiment.NEUTRAL  # Default sentiment
        self._followers_gained = 0
        self._followers_lost = 0
        self._is_spam = False  # Default is not spam
        self._is_valid = True  # Default is valid
        self.logger = LoggerService.get_logger()

        self.logger.debug(
            f"Post initialized with content: {content[:50]}..."
            if len(content) > 50
            else content
        )

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        self._author = value

    @property
    def image_path(self):
        return self._image_path

    @image_path.setter
    def image_path(self, value):
        self._image_path = value

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def likes(self):
        return self._likes

    @property
    def shares(self):
        return self._shares

    @property
    def comments(self):
        return self._comments.copy()

    @property
    def sentiment(self):
        return self._sentiment

    @sentiment.setter
    def sentiment(self, value):
        # Set the post sentiment and emit change signal
        old_sentiment = self._sentiment
        self._sentiment = value

        # Only emit if the sentiment actually changed
        if old_sentiment != value:
            self.sentiment_changed.emit(value)
            self.logger.info(f"Post sentiment set to: {value.name}")

    @property
    def followers_gained(self):
        return self._followers_gained

    @property
    def followers_lost(self):
        return self._followers_lost

    @property
    def is_spam(self):
        # Check if the post is marked as spam
        return self._is_spam

    @is_spam.setter
    def is_spam(self, value):
        # Mark the post as spam or not
        self._is_spam = value

    @property
    def is_valid(self):
        # Check if the post is valid
        return self._is_valid

    @is_valid.setter
    def is_valid(self, value):
        # Mark the post as valid or not
        self._is_valid = value

    def _increment_likes(self):
        # Increment the like count (called by PostController)
        self._likes += 1
        self.likes_changed.emit(self._likes)

    def _decrement_likes(self):
        # Decrement the like count (called by PostController)
        if self._likes > 0:
            self._likes -= 1
            self.likes_changed.emit(self._likes)

    def _increment_shares(self):
        # Increment the share count (called by PostController)
        self._shares += 1
        self.shares_changed.emit(self._shares)

    def _decrement_shares(self):
        # Decrement the share count (called by PostController)
        if self._shares > 0:
            self._shares -= 1
            self.shares_changed.emit(self._shares)

    def _add_comment(self, comment):
        # Add a comment to the post (called by PostController)
        self._comments.append(comment)
        self.comments_changed.emit(self._comments.copy())

    def _remove_comment(self, comment):
        # Remove a comment from the post (called by PostController)
        if comment in self._comments:
            self._comments.remove(comment)
            self.comments_changed.emit(self._comments.copy())

    def _add_follower_lost(self):
        # Track a follower lost due to this post
        self._followers_lost += 1
        self.followers_lost_changed.emit(self._followers_lost)
        self.logger.debug(
            f"Follower lost. Total followers lost: {self._followers_lost}"
        )

    def _add_follower_gained(self):
        # Track a follower gained due to this post
        self._followers_gained += 1
        self.followers_gained_changed.emit(self._followers_gained)
        self.logger.debug(
            f"Follower gained. Total followers gained: {self._followers_gained}"
        )

    @classmethod
    def _create(cls, content: str):
        # Factory method used by builders
        return cls(content)

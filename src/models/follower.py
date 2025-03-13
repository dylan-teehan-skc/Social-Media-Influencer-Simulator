from PyQt6.QtCore import QObject, pyqtSignal
from random import randint

from src.patterns.command.post_commands import (
    CommandHistory,
    CommentCommand,
    LikeCommand,
    ShareCommand,
)
from src.models.post import Comment, Post, Sentiment
from src.services.logger_service import LoggerService


class Follower(QObject):
    """Follower model representing a user who follows another user."""
    
    # Signals
    interaction_occurred = pyqtSignal(object, object)  # Emitted when follower interacts with a post
    unfollowed = pyqtSignal(object)  # Emitted when follower unfollows
    
    # Political lean thresholds
    LEFT_LEAN_THRESHOLD = 40
    RIGHT_LEAN_THRESHOLD = 60
    
    # Comment types
    FOLLOW_COMMENT_NEUTRAL = "Balanced take! Following for more."
    FOLLOW_COMMENT_POLITICAL = "Great content! Just followed you!"
    
    # Follower handle prefixes by sentiment
    FOLLOWER_PREFIXES = {
        "LEFT": ["progressive_", "leftist_", "socialist_", "liberal_"],
        "RIGHT": ["conservative_", "traditional_", "freedom_", "patriot_"],
        "NEUTRAL": ["moderate_", "centrist_", "balanced_", "neutral_"]
    }

    def __init__(self, sentiment: Sentiment, handle: str):
        """Initialize a follower with sentiment and handle."""
        super().__init__()
        self._handle = handle
        self.logger = LoggerService.get_logger()

        # Set initial political lean based on sentiment
        if sentiment == Sentiment.LEFT:
            self._political_lean = randint(0, 30)  # Left-leaning: 0-30
        elif sentiment == Sentiment.RIGHT:
            self._political_lean = randint(70, 100)  # Right-leaning: 70-100
        else:
            self._political_lean = randint(40, 60)  # Neutral: 40-60

        self._sentiment = sentiment  # Store the follower's sentiment
        self.command_history = CommandHistory()  # Track commands for potential undo

        self._positive_comments = [
            "Couldn't agree more!",
            "This is exactly what I've been saying!",
            "Great point!",
            "Thanks for sharing this important message!",
            "Absolutely spot on!"
        ]

        self._neutral_comments = [
            "Interesting perspective.",
            "Something to think about.",
            "I see your point.",
            "Worth considering.",
            "Thanks for sharing."
        ]

        self._negative_comments = [
            "I respectfully disagree.",
            "Not sure I can agree with this.",
            "You might want to reconsider this.",
            "I see it differently.",
            "Let's agree to disagree."
        ]

        self.logger.debug(f"Follower created: {handle} with {sentiment.name} sentiment and political lean {self._political_lean}")

    @property
    def handle(self):
        """Get the follower's handle."""
        return self._handle
        
    @property
    def sentiment(self):
        """Get the follower's sentiment."""
        return self._sentiment
        
    @property
    def political_lean(self):
        """Get the follower's political lean."""
        return self._political_lean
        
    @political_lean.setter
    def political_lean(self, value):
        """Set the follower's political lean."""
        self._political_lean = max(0, min(100, value))
        
    @classmethod
    def create_with_random_handle(cls, sentiment: Sentiment):
        """Create a follower with a randomly generated handle based on sentiment."""
        # Use the sentiment name as the key
        sentiment_name = sentiment.name
        prefixes = cls.FOLLOWER_PREFIXES[sentiment_name]
        prefix = prefixes[randint(0, len(prefixes) - 1)]
        handle = f"{prefix}{randint(1000, 9999)}"
        return cls(sentiment, handle)
        
    @classmethod
    def create_random_follower(cls, index: int):
        """Create a follower with random sentiment based on index."""
        # Get a random sentiment based on index
        sentiment_names = list(cls.FOLLOWER_PREFIXES.keys())
        sentiment_name = sentiment_names[index % len(sentiment_names)]
        
        # Convert name to Sentiment enum
        if sentiment_name == "LEFT":
            sentiment = Sentiment.LEFT
        elif sentiment_name == "RIGHT":
            sentiment = Sentiment.RIGHT
        else:
            sentiment = Sentiment.NEUTRAL
            
        return cls.create_with_random_handle(sentiment)

    # Observer pattern method (implemented directly instead of inheriting)
    def update(self, subject, post=None):
        """Handle updates from the subject (user)."""
        if post:
            # Interact with the post
            self.interact_with_post(post)
            
            # The decision to unfollow is delegated to the FollowerController
            # which will call this method and handle the result
            
        return False  # No unfollowing occurred by default
        
    def interact_with_post(self, post: Post) -> None:
        """Interact with a post based on political alignment."""
        # Calculate alignment between follower and post
        if post.sentiment == Sentiment.LEFT:
            alignment = 100 - self.political_lean  # Higher political_lean = less aligned with LEFT
        elif post.sentiment == Sentiment.RIGHT:
            alignment = self.political_lean  # Higher political_lean = more aligned with RIGHT
        else:
            # For neutral posts, alignment is based on how moderate the follower is
            # Followers closer to center (50) have higher alignment with neutral posts
            alignment = 100 - abs(50 - self.political_lean) * 2

        author_info = f"by {post.author.handle}" if post.author else "(no author)"
        self.logger.info(f"Follower {self.handle} (political lean: {self.political_lean}) has {alignment}% alignment with {post.sentiment.name} post {author_info}")

        # Emit signal for interaction
        self.interaction_occurred.emit(self, post)
        
        # The actual interaction logic (commenting, liking, sharing) is delegated to the FollowerController

from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from enum import Enum
from dotenv import load_dotenv
import os
import random
from src.services.logger_service import LoggerService

if TYPE_CHECKING:
    from src.models.user import User

try:
    from google import genai
    GOOGLE_AI_AVAILABLE = True
except ImportError:
    GOOGLE_AI_AVAILABLE = False

class Sentiment(Enum):
    LEFT = "left"
    RIGHT = "right"
    NEUTRAL = "neutral"

class Comment:
    def __init__(self, content: str, sentiment: Sentiment, authorhandle: str):
        self.content: str = content
        self.sentiment: Sentiment = sentiment
        self.timestamp: datetime = datetime.now()
        self.author: str = authorhandle

class Post:
    def __init__(self, content: str):
        self.content: str = content
        self.author = None
        self.image_path = None
        self.sentiment = None
        self.comments = []
        self.is_spam = False
        self.timestamp = datetime.now()
        self.likes: int = 0
        self.shares: int = 0
        # Track follower impact
        self.followers_gained: int = 0
        self.followers_lost: int = 0
        self.logger = LoggerService.get_logger()
        
        self.logger.debug(f"Post initialized with content: {content[:50]}..." if len(content) > 50 else content)

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("Posts can only be created through PostBuilderFactory")

    @classmethod
    def _create(cls, content: str) -> 'Post':
        """Private constructor - posts should only be created through PostBuilderFactory"""
        instance = super().__new__(cls)
        instance.__init__(content)
        return instance

    def initial_impressions(self) -> None:
        try:
            if not GOOGLE_AI_AVAILABLE:
                raise ImportError("Google AI package not available")
                
            # Load environment variables from .env file
            load_dotenv()
            API_KEY = os.getenv("GOOGLE_API_KEY")
            
            if not API_KEY:
                raise ValueError("GOOGLE_API_KEY not found in environment variables")
            
            # Try to use Google AI for sentiment analysis
            sentiment = self._analyze_content(self.content)
            
            # Convert result to Sentiment enum
            if sentiment == "left":
                self.sentiment = Sentiment.LEFT
            elif sentiment == "right":
                self.sentiment = Sentiment.RIGHT
            else:
                self.sentiment = Sentiment.NEUTRAL
                
            self.logger.info(f"Post sentiment analyzed as {self.sentiment.name}")
                
        except Exception as e:
            self.logger.warning(f"Using fallback sentiment analysis: {str(e)}")
            # Simple fallback: randomly assign sentiment for demo purposes
            self.sentiment = random.choice([Sentiment.LEFT, Sentiment.RIGHT, Sentiment.NEUTRAL])
            self.logger.info(f"Post sentiment randomly assigned as {self.sentiment.name}")

    def like(self, follower=None) -> None:
        self.likes += 1
        self.logger.debug(f"Post liked, total likes: {self.likes}")
        
    def unlike(self, follower=None) -> None:
        if self.likes > 0:
            self.likes -= 1
            self.logger.debug(f"Post unliked, total likes: {self.likes}")
        else:
            self.logger.warning("Attempted to unlike a post with 0 likes")

    def share(self, follower=None) -> None:
        self.shares += 1
        self.logger.debug(f"Post shared, total shares: {self.shares}")

    def unshare(self, follower=None) -> None:
        if self.shares > 0:
            self.shares -= 1
            self.logger.debug(f"Post unshared, total shares: {self.shares}")
        else:
            self.logger.warning("Attempted to unshare a post with 0 shares")
        
    def add_comment(self, comment: Comment) -> None:
        self.comments.append(comment)
        self.logger.debug(f"Comment added by {comment.author}: {comment.content[:30]}..." if len(comment.content) > 30 else comment.content)

    def add_follower_gained(self):
        self.followers_gained += 1
        self.logger.debug(f"Follower gained, total gained: {self.followers_gained}")
        
    def add_follower_lost(self):
        self.followers_lost += 1
        self.logger.debug(f"Follower lost, total lost: {self.followers_lost}")

    def _analyze_content(self, content: str) -> str:
        if not GOOGLE_AI_AVAILABLE:
            raise ImportError("Google AI package not available")
            
        API_KEY = os.getenv("GOOGLE_API_KEY")
        if not API_KEY:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        prompt = f"""
        Analyze the following text for political sentiment.
        Respond with exactly one word - either 'left', 'right', or 'neutral':

        Text: {content}
        """

        self.logger.debug("Sending content to Google AI for sentiment analysis")
        client = genai.Client(api_key=API_KEY)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        
        sentiment = response.text.strip().lower()
        
        # Validate the response
        if sentiment not in ["left", "right", "neutral"]:
            self.logger.warning(f"Unexpected API response: {sentiment}, defaulting to neutral")
            return "neutral"
            
        return sentiment

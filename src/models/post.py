from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from enum import Enum
from dotenv import load_dotenv
import os
import random

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
        self.timestamp: datetime = datetime.now()
        self.likes: int = 0
        self.shares: int = 0
        self.sentiment: Sentiment = Sentiment.NEUTRAL
        self.comments: List[Comment] = []
        self.author: Optional['User'] = None
        # Track follower impact
        self.followers_gained: int = 0
        self.followers_lost: int = 0
    
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
                
        except Exception as e:
            print(f"Using fallback sentiment analysis: {str(e)}")
            # Simple fallback: randomly assign sentiment for demo purposes
            self.sentiment = random.choice([Sentiment.LEFT, Sentiment.RIGHT, Sentiment.NEUTRAL])

    def like(self, follower=None) -> None:
        self.likes += 1
        
    def unlike(self, follower=None) -> None:
        self.likes -= 1

    def share(self, follower=None) -> None:
        self.shares += 1

    def unshare(self, follower=None) -> None:
        self.shares -= 1
        
    def add_comment(self, comment: Comment) -> None:
        self.comments.append(comment)

    def add_follower_gained(self):
        self.followers_gained += 1
        
    def add_follower_lost(self):
        self.followers_lost += 1

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

        client = genai.Client(api_key=API_KEY)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        
        sentiment = response.text.strip().lower()
        
        # Validate the response
        if sentiment not in ["left", "right", "neutral"]:
            print(f"Unexpected API response: {sentiment}, defaulting to neutral")
            return "neutral"
            
        return sentiment

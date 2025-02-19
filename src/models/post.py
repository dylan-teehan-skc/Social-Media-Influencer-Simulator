from datetime import datetime
from typing import List, Optional
from enum import Enum
from dotenv import load_dotenv
import os
from google import genai

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
        # user reactions will depend on sentiment
        try:
            # Placeholder for AI analysis - replace with actual AI implementation
            ai_result = self._analyze_content(self.content)
            
            # Convert AI result to Sentiment enum
            if ai_result == "left":
                self.sentiment = Sentiment.LEFT
            elif ai_result == "right":
                self.sentiment = Sentiment.RIGHT
            else:
                self.sentiment = Sentiment.NEUTRAL
                
        except Exception as e:
            # If analysis fails, default to neutral
            self.sentiment = Sentiment.NEUTRAL
            print(f"Error analyzing content: {str(e)}")

    def like(self) -> None:
        self.likes += 1
        
    def unlike(self) -> None:
        self.likes -= 1

    def share(self) -> None:
        self.shares += 1

    def unshare(self) -> None:
        self.shares -= 1

    def _analyze_content(self, content: str) -> str:
        load_dotenv()  # Load environment variables from .env file
        API_KEY = os.getenv("GOOGLE_API_KEY")
        if not API_KEY:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        prompt = f"""
        Analyze the following text for political sentiment.
        Respond with exactly one word - either 'left', 'right', or 'neutral':

        Text: {content}
        """

        try:
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

        except Exception as e:
            print(f"Error calling Google Gemini API: {str(e)}")
            return "neutral"

class Comment:
    def __init__(self, content: str, sentiment: Sentiment, authorhandle: str):
        self.content: str = content
        self.sentiment: Sentiment = sentiment
        self.timestamp: datetime = datetime.now()
        self.author: str = authorhandle

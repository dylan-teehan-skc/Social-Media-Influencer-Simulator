from enum import Enum, auto

class Sentiment(Enum):
    """Enum representing the political sentiment of content."""
    LEFT = auto()
    RIGHT = auto()
    NEUTRAL = auto()
    
    @classmethod
    def from_string(cls, sentiment_str):
        """Convert a string to a Sentiment enum value."""
        mapping = {
            "left": cls.LEFT,
            "right": cls.RIGHT,
            "neutral": cls.NEUTRAL
        }
        return mapping.get(sentiment_str.lower(), cls.NEUTRAL)
    
    def __str__(self):
        return self.name 
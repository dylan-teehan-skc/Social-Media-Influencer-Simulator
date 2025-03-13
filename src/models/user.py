from src.patterns.factory.post_builder_factory import PostBuilderFactory
from src.patterns.interfaces.observer import Observer
from src.models.post import Comment, Post, Sentiment
from src.services.logger_service import LoggerService
from PyQt6.QtCore import QObject, pyqtSignal
from datetime import datetime


class User(QObject):
    """User model representing a social media account."""
    
    # Signals
    follower_added = pyqtSignal(object)  # Emitted when a follower is added
    follower_removed = pyqtSignal(object)  # Emitted when a follower is removed
    post_created = pyqtSignal(object)  # Emitted when a post is created
    reputation_changed = pyqtSignal(int)  # Emitted when reputation changes
    
    # Reputation constants
    REPUTATION_RECOVERY_DELAY = 60000  # 60 seconds in milliseconds
    MAX_REPUTATION_PENALTY = 0.5
    REPUTATION_PENALTY_PER_LOSS = 0.1
    REPUTATION_WARNING_THRESHOLD = 5
    
    # Follower gain constants
    BASE_NEUTRAL_CHANCE = 20
    HOT_TAKE_CHANCE = 30
    MAX_FOLLOWER_MULTIPLIER = 3.0
    FOLLOWER_MULTIPLIER_SCALE = 1000
    
    def __init__(self, handle, bio):
        """Initialize a user with handle and bio."""
        super().__init__()
        self._handle = handle
        self._bio = bio
        self._followers = []
        self._posts = []
        self._follower_count = 0
        self._recent_follower_losses = 0
        self._last_reputation_check = datetime.now().timestamp() * 1000  # Convert to milliseconds
        self.logger = LoggerService.get_logger()
        self._observers = []  # For the Subject pattern
        
    @property
    def handle(self):
        """Get the user's handle."""
        return self._handle
        
    @handle.setter
    def handle(self, value):
        """Set the user's handle."""
        self._handle = value
        
    @property
    def bio(self):
        """Get the user's bio."""
        return self._bio
        
    @bio.setter
    def bio(self, value):
        """Set the user's bio."""
        self._bio = value
        
    @property
    def followers(self):
        """Get the user's followers."""
        return self._followers.copy()
        
    @property
    def follower_count(self):
        """Get the number of followers."""
        return self._follower_count
        
    @property
    def posts(self):
        """Get the user's posts."""
        return self._posts.copy()
        
    @property
    def recent_follower_losses(self):
        """Get the recent follower losses."""
        return self._recent_follower_losses

    # Subject pattern methods (implemented directly instead of inheriting)
    
    def attach(self, observer, post=None):
        """Attach an observer to the subject."""
        if observer not in self._observers:
            self._observers.append(observer)
            
    def detach(self, observer):
        """Detach an observer from the subject."""
        if observer in self._observers:
            self._observers.remove(observer)
            
    def notify(self, post=None):
        """Notify all observers about an event."""
        for observer in self._observers:
            observer.update(self, post)

    # notify_followers method has been moved to UserController

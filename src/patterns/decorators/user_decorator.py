from abc import ABC, abstractmethod
from PyQt6.QtCore import QObject, pyqtSignal

class UserDecorator(QObject, ABC):
    """Abstract decorator for User objects."""
    
    # Forward all signals from the decorated user
    follower_added = pyqtSignal(object)
    follower_removed = pyqtSignal(object)
    post_created = pyqtSignal(object)
    reputation_changed = pyqtSignal(int)
    
    def __init__(self, user):
        """Initialize with a user to decorate."""
        super().__init__()
        self._user = user
        
        # Connect signals from decorated user to this decorator's signals
        self._user.follower_added.connect(self.follower_added)
        self._user.follower_removed.connect(self.follower_removed)
        self._user.post_created.connect(self.post_created)
        self._user.reputation_changed.connect(self.reputation_changed)
    
    @property
    def handle(self):
        """Get the user's handle."""
        return self._user.handle
    
    @property
    def bio(self):
        """Get the user's bio."""
        return self._user.bio
    
    @property
    def followers(self):
        """Get the user's followers."""
        return self._user.followers
    
    @property
    def follower_count(self):
        """Get the number of followers."""
        return self._user.follower_count
    
    @property
    def posts(self):
        """Get the user's posts."""
        return self._user.posts
    
    @property
    def recent_follower_losses(self):
        """Get the recent follower losses."""
        return self._user.recent_follower_losses
    
    # Forward all methods to the decorated user
    def add_follower(self, follower, post=None):
        """Add a follower to the user."""
        return self._user.add_follower(follower, post)
    
    def remove_follower(self, follower):
        """Remove a follower from the user."""
        return self._user.remove_follower(follower)
    
    def create_post(self, content, image_path=None):
        """Create a new post."""
        return self._user.create_post(content, image_path)
    
    def calculate_follow_chance(self, post_sentiment):
        """Calculate the chance of gaining a new follower."""
        return self._user.calculate_follow_chance(post_sentiment)
    
    def update_reputation(self, initial_followers, post):
        """Update reputation based on follower losses."""
        return self._user.update_reputation(initial_followers, post)
    
    def update_reputation_recovery(self, current_time):
        """Recover reputation over time."""
        return self._user.update_reputation_recovery(current_time) 
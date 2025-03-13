from PyQt6.QtCore import QObject, pyqtSignal
from random import randint
from src.models.follower import Follower
from src.models.sentiment import Sentiment
from src.services.logger_service import LoggerService
import random

class FollowerController(QObject):
    """Controller for follower-related operations."""
    
    # Signals
    follower_added = pyqtSignal(object)  # Emitted when a follower is added
    follower_removed = pyqtSignal(object)  # Emitted when a follower is removed
    
    # Constants
    MIN_FOLLOWERS_PER_POST = 3
    MAX_FOLLOWERS_PER_POST = 10
    
    def __init__(self, user_controller, post_controller):
        """Initialize the follower controller with user and post controllers."""
        super().__init__()
        self._user_controller = user_controller
        self._post_controller = post_controller
        self._logger = LoggerService.get_logger()
        
        # Connect to post controller signals
        self._post_controller.post_created.connect(self._on_post_created)
        
    def initialize(self):
        """Initialize the follower controller."""
        self._logger.info("Follower controller initialized")
        self._create_initial_followers()
        
    def _create_initial_followers(self):
        """Create initial followers for the user."""
        initial_followers = [
            Follower(Sentiment.LEFT, "leftie_123"),
            Follower(Sentiment.RIGHT, "conservative_guy"),
            Follower(Sentiment.NEUTRAL, "centrist_person")
        ]
        
        user = self._user_controller.get_user()
        for follower in initial_followers:
            user.add_follower(follower)
            
        self._logger.info(f"Created initial followers: {[f.handle for f in initial_followers]}")
        
    def _on_post_created(self, post):
        """Handle post creation event."""
        self._logger.info(f"Processing new post with sentiment: {post.sentiment.name}")
        
        # Store the current post sentiment for follower creation
        self._current_post_sentiment = post.sentiment
        
        # Get user
        user = self._user_controller.get_user()
        
        # Calculate follow chance
        follow_chance = user.calculate_follow_chance(post.sentiment)
        self._logger.debug(f"Follow chance calculated: {follow_chance}%")
        
        # Generate and process potential followers
        self._generate_and_process_followers(post, follow_chance)
        
        # Update reputation
        initial_followers = user.follower_count
        lost_followers = user.update_reputation(initial_followers, post)
        
        if lost_followers > 0:
            self._logger.warning(f"Lost {lost_followers} followers from post")
            
    def _generate_and_process_followers(self, post, follow_chance):
        """Generate and process potential followers for a post."""
        # Calculate how many potential followers to generate
        # Increase the base number and apply a multiplier to the follow chance
        adjusted_follow_chance = min(100, follow_chance * 1.5)  # Increase follow chance by 50%
        potential_count = self.MIN_FOLLOWERS_PER_POST + int((adjusted_follow_chance / 100) * 
                                                         (self.MAX_FOLLOWERS_PER_POST - self.MIN_FOLLOWERS_PER_POST))
        
        # Add a random bonus (1-3 additional potential followers)
        potential_count += random.randint(1, 3)
        
        self._logger.debug(f"Generating {potential_count} potential followers for post with follow chance {follow_chance}%")
        
        user = self._user_controller.get_user()
        gained_followers = 0
        
        for i in range(potential_count):
            # Create a new follower
            follower = self._create_potential_follower(i)
            
            # Check if they should follow
            if follower.should_follow(post, follow_chance):
                # Add follower comment
                follower.add_follow_comment(post)
                
                # Add follower to user directly
                user.add_follower(follower, post)
                
                # Track follower gain
                post.add_follower_gained()
                gained_followers += 1
                
                # Emit signal
                self.follower_added.emit(follower)
                
        if gained_followers > 0:
            self._logger.info(f"Gained {gained_followers} new followers from post")
        else:
            self._logger.warning(f"No new followers gained from post")
            
    def _create_potential_follower(self, index):
        """Create a potential follower that's more likely to align with the post's sentiment."""
        # Create followers with a mix of sentiments, but biased toward the post's sentiment
        if hasattr(self, '_current_post_sentiment') and self._current_post_sentiment:
            # 70% chance to create a follower aligned with the post's sentiment
            if random.randint(1, 100) <= 70:
                return Follower.create_with_random_handle(self._current_post_sentiment)
        
        # Otherwise create a random follower
        return Follower.create_random_follower(index) 
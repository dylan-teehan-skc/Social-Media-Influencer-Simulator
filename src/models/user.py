from src.factory.post_builder_factory import PostBuilderFactory
from src.interfaces.observer import Observer, Subject
from src.models.post import Comment, Post, Sentiment
from src.services.logger_service import LoggerService
import pygame


class User(Subject):
    # Reputation constants
    REPUTATION_RECOVERY_DELAY = 30000  # 30 seconds
    MAX_REPUTATION_PENALTY = 0.8
    REPUTATION_PENALTY_PER_LOSS = 0.2
    REPUTATION_WARNING_THRESHOLD = 3
    
    # Follower gain constants
    BASE_NEUTRAL_CHANCE = 40
    HOT_TAKE_CHANCE = 60
    MAX_FOLLOWER_MULTIPLIER = 4.0
    FOLLOWER_MULTIPLIER_SCALE = 15
    
    def __init__(self, handle, bio):
        super().__init__()
        self.handle = handle
        self.bio = bio
        self.followers = 0
        self.posts = []
        self.logger = LoggerService.get_logger()
        
        # Reputation tracking
        self.recent_follower_losses = 0
        self.last_reputation_check = pygame.time.get_ticks()

    def attach(self, observer: Observer, post=None):
        """Attach an observer to this subject.
        
        Args:
            observer: The observer to attach
            post: Optional post that attracted this follower
        """
        if observer not in self._observers:
            self._observers.append(observer)
            self.followers += 1
            
            # If a specific post attracted this follower, notify them about it
            if post:
                observer.update(self, post)

    def detach(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)
            self.followers -= 1

    def notify(self, post=None):
        for observer in self._observers:
            observer.update(self, post)

    def create_post(self, content: str, image_path: str = None) -> Post:
        # Get the appropriate builder from the factory
        post_type = "image" if image_path else "text"
        post_builder = PostBuilderFactory.get_builder(post_type)

        # Build the post using the builder
        post = post_builder\
            .set_content(content)\
            .set_author(self)

        # Set image if provided
        if image_path:
            post = post.set_image(image_path)

        # Build and finalize the post
        post = post.build()
        post.initial_impressions()  # Analyze sentiment

        # Add to posts list and notify observers
        self.posts.append(post)
        self.notify(post)

        return post

    def calculate_follow_chance(self, post_sentiment):
        """Calculate the chance of gaining a new follower based on reputation and post sentiment."""
        reputation_penalty = min(
            self.MAX_REPUTATION_PENALTY,
            self.recent_follower_losses * self.REPUTATION_PENALTY_PER_LOSS
        )
        base_chance = (
            self.BASE_NEUTRAL_CHANCE if post_sentiment == Sentiment.NEUTRAL
            else self.HOT_TAKE_CHANCE
        ) * (1 - reputation_penalty)
        follower_multiplier = min(
            self.MAX_FOLLOWER_MULTIPLIER,
            1.0 + (self.followers / self.FOLLOWER_MULTIPLIER_SCALE)
        )
        return int(base_chance * follower_multiplier)
        
    def update_reputation(self, initial_followers, post):
        """Update reputation based on follower losses from a post."""
        final_followers = self.followers
        if final_followers < initial_followers:
            lost_followers = initial_followers - final_followers
            self.recent_follower_losses += lost_followers

            self.logger.warning(
                "Lost %d followers. Total recent losses: %d",
                lost_followers,
                self.recent_follower_losses
            )

            if self.recent_follower_losses >= self.REPUTATION_WARNING_THRESHOLD:
                post.add_comment(Comment(
                    "Your recent posts are driving followers away...",
                    Sentiment.NEUTRAL,
                    "system_warning"
                ))
                self.logger.warning(
                    "Reputation warning threshold reached: %d",
                    self.recent_follower_losses
                )
                
    def update_reputation_recovery(self, current_time):
        """Recover reputation over time."""
        if current_time - self.last_reputation_check >= self.REPUTATION_RECOVERY_DELAY:
            if self.recent_follower_losses > 0:
                old_losses = self.recent_follower_losses
                self.recent_follower_losses = max(0, self.recent_follower_losses - 1)
                self.logger.info(
                    "Reputation recovered: losses decreased from %d to %d",
                    old_losses,
                    self.recent_follower_losses
                )
            self.last_reputation_check = current_time

    def edit_post(self, post):
        pass

    def delete_post(self, post):
        pass

    def follow(self, user):
        pass

    def unfollow(self, user):
        pass

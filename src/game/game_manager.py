from random import randint

import pygame

from src.interceptors.dispatcher import Dispatcher
from src.interceptors.spam_filter import SpamFilter
from src.models.follower import Follower
from src.models.post import Comment, Sentiment
from src.models.user import User
from src.services.logger_service import LoggerService


# pylint: disable=R0902
class GameManager:
    MIN_FOLLOWERS_PER_POST = 1
    MAX_FOLLOWERS_PER_POST = 5

    def __init__(self, mediator):
        self.mediator = mediator
        self.mediator.set_game_manager(self)
        self.logger = LoggerService.get_logger()
        self.user = User("sloggo", "I'm a software engineer")
        
        # Create dispatcher with spam filter
        self.dispatcher = Dispatcher()
        self.dispatcher.add_interceptor(SpamFilter())
        
        # Create initial followers
        self.create_initial_followers()
        
        self.logger.info("GameManager initialized with user %s", self.user.handle)

    def create_initial_followers(self):
        initial_followers = [
            Follower(Sentiment.LEFT, "leftie_123"),
            Follower(Sentiment.RIGHT, "conservative_guy"),
            Follower(Sentiment.NEUTRAL, "centrist_person")
        ]
        for follower in initial_followers:
            # For initial followers, we don't have a specific post that attracted them
            self.user.attach(follower, None)
        self.logger.info("Created initial followers: %s", [f.handle for f in initial_followers])

    def create_potential_follower(self, index):
        return Follower.create_random_follower(index)

    def calculate_follow_chance(self, post_sentiment):
        return self.user.calculate_follow_chance(post_sentiment)

    def handle_post_creation(self, content: str, image_path: str = None):
        # Create post through User class which uses PostBuilderFactory
        post = self.user.create_post(content, image_path)
        self.dispatcher.process_post(post)  # Process the post through the dispatcher

        if post.is_spam:
            self.mediator.get_ui_logic().show_notification(
                "Post rejected: content is considered spam."
            )
            return

        view = self.mediator.get_view()
        view.posts.insert(0, post)

        initial_followers = self.user.followers
        follow_chance = self.calculate_follow_chance(post.sentiment)

        self.logger.info(
            "New post created by %s with sentiment %s",
            self.user.handle,
            post.sentiment)
        self.logger.debug("Follow chance calculated: %d%%", follow_chance)

        self.generate_and_process_followers(post, follow_chance)
        self.user.update_reputation(initial_followers, post)

    def generate_and_process_followers(self, post, follow_chance):
        """Generate and process new followers based on post quality and follow chance."""
        # Calculate how many potential followers to generate based on follow chance
        # Higher follow chance = more potential followers
        potential_count = self.MIN_FOLLOWERS_PER_POST + int((follow_chance / 100) * 
                                                          (self.MAX_FOLLOWERS_PER_POST - self.MIN_FOLLOWERS_PER_POST))
        
        self.logger.debug("Generating %d potential followers for post", potential_count)
        
        gained_followers = 0
        for i in range(potential_count):
            # Create a new follower
            follower = self.create_potential_follower(i)
            
            # Check if they should follow
            if follower.should_follow(post, follow_chance):
                # Add follower comment before attaching to avoid duplicate interactions
                follower.add_follow_comment(post)
                
                # Attach follower to user and pass the post that attracted them
                self.user.attach(follower, post)
                
                # Track follower gain in post stats
                post.add_follower_gained()
                gained_followers += 1

        if gained_followers > 0:
            self.logger.info("Gained %d new followers from post", gained_followers)

    def update_game_state(self):
        # Handle reputation recovery
        current_time = pygame.time.get_ticks()
        self.user.update_reputation_recovery(current_time)

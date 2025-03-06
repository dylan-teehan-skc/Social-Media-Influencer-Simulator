import pygame
from random import randint
from ..models.user import User
from ..models.post import Sentiment, Comment, Post
from ..models.follower import Follower
from src.interceptors.dispatcher import Dispatcher
from src.interceptors.spam_filter import SpamFilter
from ..services.logger_service import LoggerService

class GameManager:
    FOLLOWER_REFRESH_DELAY = 10000 
    REPUTATION_RECOVERY_DELAY = 30000  
    MAX_POTENTIAL_FOLLOWERS = 15
    NEW_FOLLOWERS_BATCH_SIZE = 5
    BASE_NEUTRAL_CHANCE = 40
    HOT_TAKE_CHANCE = 60 
    MAX_REPUTATION_PENALTY = 0.8
    REPUTATION_PENALTY_PER_LOSS = 0.2
    MAX_FOLLOWER_MULTIPLIER = 4.0
    FOLLOWER_MULTIPLIER_SCALE = 15
    REPUTATION_WARNING_THRESHOLD = 3
    RIGHT_LEAN_THRESHOLD = 60
    LEFT_LEAN_THRESHOLD = 40

    def __init__(self, mediator):
        self.mediator = mediator
        self.mediator.set_game_manager(self)
        self.logger = LoggerService.get_logger()
        
        self.user = User("PA", "I'm a stud")
        self.create_initial_followers()
        
        self.potential_followers = [self.create_potential_follower(i) for i in range(10)]
        self.last_follower_refresh = pygame.time.get_ticks()
        self.recent_follower_losses = 0
        self.last_reputation_check = pygame.time.get_ticks()
        self.reputation_recovery_delay = 30000  # 30 seconds to start recovering reputation
        
        self.dispatcher = Dispatcher()  # Create a dispatcher instance
        self.dispatcher.add_interceptor(SpamFilter())  # Add the spam filter interceptor
                
        self.logger.info("GameManager initialized with user %s", self.user.handle)

    def create_initial_followers(self):
        initial_followers = [
            Follower(Sentiment.LEFT, "leftie_123"),
            Follower(Sentiment.RIGHT, "conservative_guy"),
            Follower(Sentiment.NEUTRAL, "centrist_person")
        ]
        for follower in initial_followers:
            self.user.attach(follower)
        self.logger.info("Created initial followers: %s", [f.handle for f in initial_followers])

    def create_potential_follower(self, index):
        follower_types = {
            Sentiment.LEFT: ["progressive_", "leftist_", "socialist_", "liberal_"],
            Sentiment.RIGHT: ["conservative_", "traditional_", "freedom_", "patriot_"],
            Sentiment.NEUTRAL: ["moderate_", "centrist_", "balanced_", "neutral_"]
        }
        sentiment = list(follower_types.keys())[index % 3]
        prefixes = follower_types[sentiment]
        prefix = prefixes[randint(0, len(prefixes) - 1)]
        return Follower(sentiment, f"{prefix}{randint(1000, 9999)}")

    def calculate_follow_chance(self, post_sentiment):
        reputation_penalty = min(self.MAX_REPUTATION_PENALTY, 
                               self.recent_follower_losses * self.REPUTATION_PENALTY_PER_LOSS)
        base_chance = (self.BASE_NEUTRAL_CHANCE if post_sentiment == Sentiment.NEUTRAL 
                      else self.HOT_TAKE_CHANCE) * (1 - reputation_penalty)
        follower_multiplier = min(self.MAX_FOLLOWER_MULTIPLIER, 
                                1.0 + (self.user.followers / self.FOLLOWER_MULTIPLIER_SCALE))
        return int(base_chance * follower_multiplier)

    def should_follower_follow(self, follower, post, follow_chance):
        if post.sentiment == Sentiment.NEUTRAL:
            return randint(1, 100) <= follow_chance
        
        return ((follower.political_lean > self.RIGHT_LEAN_THRESHOLD and post.sentiment == Sentiment.RIGHT) or
                (follower.political_lean < self.LEFT_LEAN_THRESHOLD and post.sentiment == Sentiment.LEFT)) and \
               randint(1, 100) <= follow_chance

    def add_follower_comment(self, post, follower):
        comment_text = ("Balanced take! Following for more." if post.sentiment == Sentiment.NEUTRAL
                       else "Great content! Just followed you!")
        post.add_comment(Comment(comment_text, follower.sentiment, follower.handle))

    def handle_post_creation(self, content: str, image_path: str = None):
        # Create post through User class which uses PostBuilderFactory
        post = self.user.create_post(content, image_path)
        self.dispatcher.process_post(post)  # Process the post through the dispatcher

        if post.is_spam:
            self.mediator.get_ui_logic().show_notification("Post rejected: content is considered spam.")
            return
        else: 
            view = self.mediator.get_view()
            view.posts.insert(0, post)

        initial_followers = self.user.followers
        follow_chance = self.calculate_follow_chance(post.sentiment)
        
        self.logger.info("New post created by %s with sentiment %s", self.user.handle, post.sentiment)
        self.logger.debug("Follow chance calculated: %d%%", follow_chance)
        
        self.process_potential_followers(post, follow_chance)
        self.update_reputation(initial_followers, post)

    def process_potential_followers(self, post, follow_chance):
        if not self.potential_followers:
            self.logger.debug("No potential followers available")
            return

        gained_followers = 0
        for i in range(len(self.potential_followers) - 1, -1, -1):
            follower = self.potential_followers[i]
            if self.should_follower_follow(follower, post, follow_chance):
                self.user.attach(follower)
                follower.interact_with_post(post)
                self.add_follower_comment(post, follower)
                self.potential_followers.pop(i)
                post.add_follower_gained()
                gained_followers += 1
        
        if gained_followers > 0:
            self.logger.info("Gained %d new followers from post", gained_followers)

    def update_reputation(self, initial_followers, post):
        final_followers = self.user.followers
        if final_followers < initial_followers:
            lost_followers = initial_followers - final_followers
            self.recent_follower_losses += lost_followers
            
            self.logger.warning("Lost %d followers. Total recent losses: %d", 
                              lost_followers, self.recent_follower_losses)
            
            if self.recent_follower_losses >= self.REPUTATION_WARNING_THRESHOLD:
                post.add_comment(Comment(
                    "Your recent posts are driving followers away...",
                    Sentiment.NEUTRAL,
                    "system_warning"
                ))
                self.logger.warning("Reputation warning threshold reached: %d", 
                                  self.recent_follower_losses)

    def update_potential_followers(self):
        current_time = pygame.time.get_ticks()
        self.update_reputation_recovery(current_time)
        self.refresh_follower_pool(current_time)

    def update_reputation_recovery(self, current_time):
        if current_time - self.last_reputation_check >= self.REPUTATION_RECOVERY_DELAY:
            if self.recent_follower_losses > 0:
                old_losses = self.recent_follower_losses
                self.recent_follower_losses = max(0, self.recent_follower_losses - 1)
                self.logger.info("Reputation recovered: losses decreased from %d to %d", 
                               old_losses, self.recent_follower_losses)
            self.last_reputation_check = current_time

    def refresh_follower_pool(self, current_time):
        if current_time - self.last_follower_refresh >= self.FOLLOWER_REFRESH_DELAY:
            if len(self.potential_followers) < self.MAX_POTENTIAL_FOLLOWERS:
                new_followers_count = min(
                    self.NEW_FOLLOWERS_BATCH_SIZE,
                    self.MAX_POTENTIAL_FOLLOWERS - len(self.potential_followers)
                )
                for i in range(new_followers_count):
                    self.potential_followers.append(
                        self.create_potential_follower(len(self.potential_followers))
                    )
                self.logger.info("Refreshed follower pool with %d new potential followers", 
                               new_followers_count)
            self.last_follower_refresh = current_time
            
            
    
import pygame
from random import randint
from ..models.user import User
from ..models.post import Sentiment, Comment
from ..models.follower import Follower

class GameManager:
    def __init__(self, mediator):
        
        #mediator
        self.mediator = mediator
        self.mediator.set_game_manager(self)

        # Create main user
        self.user = User("PA", "I'm a stud")
        
        # Create initial followers
        self.create_initial_followers()
        
        # Create potential followers pool
        self.potential_followers = [self.create_potential_follower(i) for i in range(10)]
        self.last_follower_refresh = pygame.time.get_ticks()
        self.follower_refresh_delay = 10000
        
        # Track reputation (follower losses)
        self.recent_follower_losses = 0
        self.last_reputation_check = pygame.time.get_ticks()
        self.reputation_recovery_delay = 30000  # 30 seconds to start recovering reputation
                
    def create_initial_followers(self):
        followers = [
            Follower(Sentiment.LEFT, "leftie_123"),
            Follower(Sentiment.RIGHT, "conservative_guy"),
            Follower(Sentiment.NEUTRAL, "centrist_person")
        ]
        for follower in followers:
            self.user.attach(follower)
            
    def create_potential_follower(self, index):
        follower_types = [
            (Sentiment.LEFT, ["progressive_", "leftist_", "socialist_", "liberal_"]),
            (Sentiment.RIGHT, ["conservative_", "traditional_", "freedom_", "patriot_"]),
            (Sentiment.NEUTRAL, ["moderate_", "centrist_", "balanced_", "neutral_"])
        ]
        sentiment, prefixes = follower_types[index % 3]
        prefix = prefixes[randint(0, len(prefixes) - 1)]
        return Follower(sentiment, f"{prefix}{randint(1000, 9999)}")
        
    def handle_post_creation(self, content: str):
        post = self.user.create_post(content)
        view = self.mediator.get_view()
        view.posts.insert(0, post)
        
        # Base chances affected by reputation
        reputation_penalty = min(0.8, self.recent_follower_losses * 0.2)  # Each loss reduces chances by 20%, up to 80%
        base_chance = (40 if post.sentiment == Sentiment.NEUTRAL else 60) * (1 - reputation_penalty)
        follower_multiplier = min(4.0, 1.0 + (self.user.followers / 15))
        follow_chance = int(base_chance * follower_multiplier)
        
        # Track follower losses from this post
        initial_followers = self.user.followers
        
        # Chance to gain new followers based on post sentiment
        if self.potential_followers:
            for i in range(len(self.potential_followers) - 1, -1, -1):
                follower = self.potential_followers[i]
                should_follow = False
                
                if post.sentiment == Sentiment.NEUTRAL:
                    should_follow = randint(1, 100) <= follow_chance
                else:
                    if (follower.political_lean > 60 and post.sentiment == Sentiment.RIGHT) or \
                       (follower.political_lean < 40 and post.sentiment == Sentiment.LEFT):
                        should_follow = randint(1, 100) <= follow_chance
                
                if should_follow:
                    self.user.attach(follower)
                    follower.interact_with_post(post)
                    if post.sentiment == Sentiment.NEUTRAL:
                        post.add_comment(Comment("Balanced take! Following for more.", follower.sentiment, follower.handle))
                    else:
                        post.add_comment(Comment("Great content! Just followed you!", follower.sentiment, follower.handle))
                    self.potential_followers.pop(i)
                    post.add_follower_gained()
        
        # Update reputation based on follower losses
        final_followers = self.user.followers
        if final_followers < initial_followers:
            lost_followers = initial_followers - final_followers
            self.recent_follower_losses += lost_followers
            # Add warning comment if reputation is getting bad
            if self.recent_follower_losses >= 3:
                post.add_comment(Comment("Your recent posts are driving followers away...", 
                                      Sentiment.NEUTRAL, "system_warning"))
        
    def update_potential_followers(self):
        current_time = pygame.time.get_ticks()
        
        # Update reputation
        if current_time - self.last_reputation_check >= self.reputation_recovery_delay:
            if self.recent_follower_losses > 0:
                self.recent_follower_losses = max(0, self.recent_follower_losses - 1)  # Slowly recover reputation
            self.last_reputation_check = current_time
        
        # Regular follower pool refresh
        if current_time - self.last_follower_refresh >= self.follower_refresh_delay:
            if len(self.potential_followers) < 15:
                new_followers_count = min(5, 15 - len(self.potential_followers))
                for i in range(new_followers_count):
                    self.potential_followers.append(self.create_potential_follower(len(self.potential_followers)))
            self.last_follower_refresh = current_time
            
            
    
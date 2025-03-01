import pygame
from random import randint
from datetime import datetime
from ..models.user import User
from ..models.post import Post, Sentiment, Comment
from ..models.follower import Follower
from ..views.main_view import MainView

class GameManager:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        pygame.font.init()
        
        # Create main user
        self.user = User("sloggo", "I'm a software engineer")
        
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
        
        # Create UI
        self.view = MainView(1200, 800)
        self.clock = pygame.time.Clock()
        
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
        self.view.posts.insert(0, post)
        
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
            
    def handle_mouse_wheel(self, event):
        scroll_amount = 40  # Increased from 20 for smoother scrolling
        
        if self.view.viewing_comments:
            # Scroll up (button 4) should show more content above (negative scroll)
            # Scroll down (button 5) should show more content below (positive scroll)
            if event.button == 4:  # Scroll up
                self.view.comments_scroll_y = min(0, self.view.comments_scroll_y + scroll_amount)
            else:  # Scroll down
                # Don't allow scrolling past the last comment
                if len(self.view.current_post.comments) * 100 > 800:  # If comments exceed view height
                    max_scroll = -(len(self.view.current_post.comments) * 100 - 700)  # Leave some space at bottom
                    self.view.comments_scroll_y = max(max_scroll, self.view.comments_scroll_y - scroll_amount)
        else:
            # Same logic for main feed
            if event.button == 4:  # Scroll up
                self.view.scroll_y = min(0, self.view.scroll_y + scroll_amount)
            else:  # Scroll down
                if len(self.view.posts) * 200 > 800:  # If posts exceed view height
                    max_scroll = -(len(self.view.posts) * 200 - 700)  # Leave some space at bottom
                    self.view.scroll_y = max(max_scroll, self.view.scroll_y - scroll_amount)
            
    def handle_mouse_click(self, pos):
        if self.view.viewing_comments:
            _, back_button = self.view.draw(self.user, self.view.posts)
            if back_button.collidepoint(pos):
                self.view.viewing_comments = False
                self.view.current_post = None
                
        elif self.view.composing:
            _, tweet_button = self.view.draw(self.user, self.view.posts)
            if tweet_button.collidepoint(pos) and self.view.compose_text:
                self.handle_post_creation(self.view.compose_text)
                self.view.compose_text = ""
                self.view.composing = False
                
        else:
            post_rects, compose_button = self.view.draw(self.user, self.view.posts)
            if compose_button.collidepoint(pos):
                self.view.composing = True
            else:
                for rect, post in post_rects:
                    if rect.collidepoint(pos):
                        self.view.viewing_comments = True
                        self.view.current_post = post
                        break
                        
    def handle_key_press(self, event):
        if not self.view.composing:
            return
            
        if event.key == pygame.K_RETURN and not (event.mod & pygame.KMOD_SHIFT):
            if self.view.compose_text:
                self.handle_post_creation(self.view.compose_text)
                self.view.compose_text = ""
                self.view.composing = False
        elif event.key == pygame.K_BACKSPACE:
            self.view.compose_text = self.view.compose_text[:-1]
        elif event.key == pygame.K_ESCAPE:
            self.view.composing = False
            self.view.compose_text = ""
        else:
            self.view.compose_text += event.unicode
            
    def run(self):
        running = True
        while running:
            self.update_potential_followers()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button in (4, 5):
                        self.handle_mouse_wheel(event)
                    elif event.button == 1:
                        self.handle_mouse_click(pygame.mouse.get_pos())
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_press(event)
            
            # Draw UI
            self.view.draw(self.user, self.view.posts)
            pygame.display.flip()
            self.clock.tick(60)
            
        pygame.quit() 
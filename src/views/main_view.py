import pygame
from . import colors
from .components import Button, Post, Comment

class MainView:
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Twitter-like Social Media")
        
        # Initialize posts list
        self.posts = []
        
        # Fonts
        self.fonts = {
            'title': pygame.font.SysFont('Arial', 24, bold=True),
            'normal': pygame.font.SysFont('Arial', 16),
            'small': pygame.font.SysFont('Arial', 14)
        }
        
        # UI State
        self.scroll_y = 0
        self.composing = False
        self.compose_text = ""
        self.viewing_comments = False
        self.current_post = None
        self.comments_scroll_y = 0
        
        # Layout
        self.sidebar_width = 300
        self.content_padding = 20
        self.post_width = screen_width - self.sidebar_width - (self.content_padding * 2)
        
    def draw_sidebar(self, user):
        # Sidebar background
        sidebar_rect = pygame.Rect(0, 0, self.sidebar_width, self.height)
        pygame.draw.rect(self.screen, colors.BG_SECONDARY, sidebar_rect)
        pygame.draw.line(self.screen, colors.BORDER_COLOR, 
                        (self.sidebar_width, 0), 
                        (self.sidebar_width, self.height))
        
        # Profile section
        profile_y = 50
        profile_text = self.fonts['title'].render(f"@{user.handle}", True, colors.TEXT_PRIMARY)
        self.screen.blit(profile_text, (20, profile_y))
        
        bio_text = self.fonts['normal'].render(user.bio, True, colors.TEXT_SECONDARY)
        self.screen.blit(bio_text, (20, profile_y + 40))
        
        followers_text = self.fonts['normal'].render(f"Followers: {user.followers}", True, colors.TEXT_SECONDARY)
        self.screen.blit(followers_text, (20, profile_y + 70))
        
        # New post button
        self.compose_button = Button(
            20, profile_y + 120, 
            self.sidebar_width - 40, 50, 
            "Tweet", self.fonts['normal']
        )
        self.compose_button.draw(self.screen)
        
    def draw_compose_modal(self):
        # Dark overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(128)
        overlay.fill(colors.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Compose modal
        modal_width = 600
        modal_height = 300
        x = (self.width - modal_width) // 2
        y = (self.height - modal_height) // 2
        
        modal_rect = pygame.Rect(x, y, modal_width, modal_height)
        pygame.draw.rect(self.screen, colors.BG_SECONDARY, modal_rect, border_radius=15)
        
        # Title
        title_text = self.fonts['title'].render("Compose Tweet", True, colors.TEXT_PRIMARY)
        self.screen.blit(title_text, (x + 20, y + 20))
        
        # Text area
        text_area = pygame.Rect(x + 20, y + 70, modal_width - 40, 150)
        pygame.draw.rect(self.screen, colors.BG_MAIN, text_area, border_radius=10)
        
        if self.compose_text:
            text_surface = self.fonts['normal'].render(self.compose_text, True, colors.TEXT_PRIMARY)
            self.screen.blit(text_surface, (x + 30, y + 80))
        else:
            placeholder = self.fonts['normal'].render("What's happening?", True, colors.TEXT_SECONDARY)
            self.screen.blit(placeholder, (x + 30, y + 80))
        
        # Tweet button
        self.tweet_button = Button(
            x + modal_width - 120, y + modal_height - 60,
            100, 40, "Tweet", self.fonts['normal']
        )
        self.tweet_button.draw(self.screen)
        
        return self.tweet_button.rect
        
    def draw_comments_modal(self):
        # Dark overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(128)
        overlay.fill(colors.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Comments modal
        modal_width = 600
        modal_height = 500
        x = (self.width - modal_width) // 2
        y = (self.height - modal_height) // 2
        
        modal_rect = pygame.Rect(x, y, modal_width, modal_height)
        pygame.draw.rect(self.screen, colors.BG_SECONDARY, modal_rect, border_radius=15)
        
        # Back button
        self.back_button = Button(
            x + 20, y + 20, 80, 30,
            "Back", self.fonts['normal']
        )
        self.back_button.draw(self.screen)
        
        # Original post
        post_y = y + 70
        post = Post(self.current_post, self.fonts, width=modal_width - 40)
        post.draw(self.screen, x + 20, post_y)
        
        # Comments
        comments_y = post_y + post.height + 20
        for comment in self.current_post.comments:
            if comments_y + 80 < y + modal_height - 20:  # Only draw visible comments
                comment_ui = Comment(comment, self.fonts, width=modal_width - 40)
                comment_ui.draw(self.screen, x + 20, comments_y)
                comments_y += 90
                
        return self.back_button.rect
        
    def draw_feed(self, posts):
        feed_x = self.sidebar_width + self.content_padding
        feed_y = self.content_padding + self.scroll_y
        post_spacing = 10
        post_rects = []
        
        for post_data in posts:
            post = Post(post_data, self.fonts, width=self.post_width)
            post_rect = post.draw(self.screen, feed_x, feed_y)
            post_rects.append((post_rect, post_data))
            feed_y += post.height + post_spacing
            
        return post_rects
        
    def draw(self, user, posts):
        # Fill background
        self.screen.fill(colors.BG_MAIN)
        
        # Draw sidebar
        self.draw_sidebar(user)
        
        if self.viewing_comments:
            back_button = self.draw_comments_modal()
            return [], back_button
        elif self.composing:
            tweet_button = self.draw_compose_modal()
            return [], tweet_button
        else:
            # Draw main feed
            post_rects = self.draw_feed(posts)
            return post_rects, self.compose_button.rect 
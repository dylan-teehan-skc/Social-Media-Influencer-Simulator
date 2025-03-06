import pygame
from . import colors
from .components import Button, Post, Comment

class MainView:
    """
    This Main UI class handles the overall layout.
    It manages the screen, sidebar, and feed.

    it handles various UI states:

    - scroll_y: how far down the feed the user has scrolled.
    - composing: whether the user is creating a new tweet.
    - compose_text: the text being written for a new tweet.
    - viewing_comments: whether the user is viewing comments on a post.
    - current_post: the post whose comments the user is viewing.
    - comments_scroll_y: how far down the comments the user has scrolled.
    - selected_image: the path to an image the user has selected for a tweet.
    - image_preview: the loaded preview of the selected image.

    """
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Twitter-like Social Media")
        
        
        self.posts = []
        
        self.fonts = {
            'title': pygame.font.SysFont('Arial', 24, bold=True),
            'normal': pygame.font.SysFont('Arial', 16),
            'small': pygame.font.SysFont('Arial', 14)
        }
        
        # The UI State
        self.scroll_y = 0
        self.composing = False
        self.compose_text = ""
        self.viewing_comments = False
        self.current_post = None
        self.comments_scroll_y = 0
        self.selected_image = None
        self.image_preview = None
        
        # Layout
        self.sidebar_width = 300
        self.content_padding = 20
        self.post_width = screen_width - self.sidebar_width - (self.content_padding * 2)
        
    def draw_sidebar(self, user):
        """
        This draws the sidebar on the screen. (left side)
        It draws the sidebar background, profile section, and new post button.

        """
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
        """
        This draws the compose modal on the screen. (dialog box for creating a new tweet)
        contains all the UI elements needed to create a new tweet.
       
        """
        # Dark overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(128)
        overlay.fill(colors.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Compose modal
        modal_width = 600
        modal_height = 400  
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
            
        # Image preview area
        if self.image_preview:
            preview_rect = pygame.Rect(x + 20, y + 240, modal_width - 40, 100)
            pygame.draw.rect(self.screen, colors.BG_MAIN, preview_rect, border_radius=10)
            preview_width = preview_rect.width - 20
            preview_height = preview_rect.height - 20
            scaled_image = pygame.transform.scale(self.image_preview, (preview_width, preview_height))
            self.screen.blit(scaled_image, (x + 30, y + 250))
            
        # Image upload button
        self.upload_button = Button(
            x + 20, y + 350,
            150, 40, "Upload Image", self.fonts['normal']
        )
        self.upload_button.draw(self.screen)
        
        # Tweet button
        self.tweet_button = Button(
            x + modal_width - 120, y + modal_height - 60,
            100, 40, "Tweet", self.fonts['normal']
        )
        self.tweet_button.draw(self.screen)
        
        return self.tweet_button.rect, self.upload_button.rect
        
    def draw_comments_modal(self):
        """
        This draws the comments modal on the screen. (dialog box for viewing comments on a post)
        contains all the UI elements needed to view comments on a post.
       
        """
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
        
        # Comments section with scrolling
        comments_start_y = post_y + post.height + 20
        comments_viewport_height = max(50, modal_height - (comments_start_y - y) - 20)  # Ensures the minimum height
        
        # Create a surface for comments with minimum dimensions
        total_comments_height = max(50, len(self.current_post.comments) * 90)
        comments_surface = pygame.Surface((max(1, modal_width - 40), total_comments_height))
        comments_surface.fill(colors.BG_SECONDARY)
        comments_surface.set_colorkey(colors.BG_SECONDARY)  #This makes the background transparent
        
        # Draw comments on the surface
        current_y = 0
        for comment in self.current_post.comments:
            comment_ui = Comment(comment, self.fonts, width=modal_width - 40)
            comment_ui.draw(comments_surface, 0, current_y)
            current_y += 90
            
        # Calculate max scroll with bounds checking
        max_scroll = max(0, current_y - comments_viewport_height)
        self.comments_scroll_y = min(0, max(-max_scroll, self.comments_scroll_y))
        
        # Create a viewport surface with guaranteed valid dimensions
        viewport_surface = pygame.Surface((max(1, modal_width - 40), max(1, comments_viewport_height)))
        viewport_surface.fill(colors.BG_SECONDARY)
        viewport_rect = pygame.Rect(x + 20, comments_start_y, modal_width - 40, comments_viewport_height)
        
        # Draw the scrollable comments onto the viewport surface
        viewport_surface.blit(comments_surface, (0, self.comments_scroll_y))
        
        # Draw the viewport surface onto the screen
        self.screen.blit(viewport_surface, viewport_rect)
        
        # Draw scroll indicators if needed
        if current_y > comments_viewport_height:
            scroll_percent = abs(self.comments_scroll_y) / max_scroll
            indicator_height = (comments_viewport_height / current_y) * comments_viewport_height
            indicator_y = comments_start_y + (scroll_percent * (comments_viewport_height - indicator_height))
            
            # Draw scroll bar background
            pygame.draw.rect(self.screen, colors.BG_HOVER,
                           (x + modal_width - 25, comments_start_y, 5, comments_viewport_height))
            
            # Draw scroll bar indicator
            pygame.draw.rect(self.screen, colors.PRIMARY,
                           (x + modal_width - 25, indicator_y, 5, indicator_height))
                
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
        self.screen.fill(colors.BG_MAIN)
        
        self.draw_sidebar(user)
        
        if self.viewing_comments:
            back_button = self.draw_comments_modal()
            return [], back_button
        elif self.composing:
            tweet_button, upload_button = self.draw_compose_modal()
            return [], tweet_button, upload_button
        else:
            # Draw main feed
            post_rects = self.draw_feed(posts)
            return post_rects, self.compose_button.rect 
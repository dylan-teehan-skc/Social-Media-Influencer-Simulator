import pygame
from . import colors

class Button:
    def __init__(self, x, y, width, height, text, font, bg_color=colors.PRIMARY, text_color=colors.WHITE, border_radius=20):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_radius = border_radius
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=self.border_radius)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Post:
    # Standard image dimensions
    STANDARD_IMAGE_WIDTH = 500
    STANDARD_IMAGE_HEIGHT = 300

    def __init__(self, post_data, fonts, width=600, padding=15):
        self.post = post_data
        self.fonts = fonts
        self.width = width
        self.padding = padding
        self.image = None
        if hasattr(self.post, 'image_path') and self.post.image_path:
            try:
                self.image = pygame.image.load(self.post.image_path)
                # Scale image to standard size while maintaining aspect ratio
                image_width = self.STANDARD_IMAGE_WIDTH
                image_height = self.STANDARD_IMAGE_HEIGHT
                
                # Calculate scaling to fit within standard dimensions while maintaining aspect ratio
                img_ratio = self.image.get_width() / self.image.get_height()
                std_ratio = self.STANDARD_IMAGE_WIDTH / self.STANDARD_IMAGE_HEIGHT
                
                if img_ratio > std_ratio:  # Image is wider
                    image_width = self.STANDARD_IMAGE_WIDTH
                    image_height = int(image_width / img_ratio)
                else:  # Image is taller
                    image_height = self.STANDARD_IMAGE_HEIGHT
                    image_width = int(image_height * img_ratio)
                
                self.image = pygame.transform.scale(self.image, (image_width, image_height))
            except Exception as e:
                print(f"Error loading image: {e}")
        self.height = self.calculate_height()
        
    def calculate_height(self):
        # Base height for padding and fixed elements
        height = 140  # Increased to accommodate new stats
        
        # Add height for wrapped text
        content_width = self.width - (self.padding * 2)
        words = self.post.content.split()
        line = ""
        num_lines = 1
        
        for word in words:
            test_line = line + word + " "
            test_surface = self.fonts['normal'].render(test_line, True, colors.TEXT_PRIMARY)
            if test_surface.get_width() > content_width:
                num_lines += 1
                line = word + " "
            else:
                line = test_line
                
        # Add height for image if present
        if self.image:
            height += self.image.get_height() + self.padding
                
        return height + (num_lines * 25)
        
    def draw(self, screen, x, y):
        # Post container
        post_rect = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(screen, colors.BG_SECONDARY, post_rect)
        pygame.draw.rect(screen, colors.BORDER_COLOR, post_rect, 1)
        
        current_y = y + self.padding
        
        # Author info
        author_text = self.fonts['normal'].render(f"@{self.post.author.handle}", True, colors.TEXT_PRIMARY)
        screen.blit(author_text, (x + self.padding, current_y))
        
        # Timestamp
        time_text = self.fonts['small'].render(self.post.timestamp.strftime('%I:%M %p'), True, colors.TEXT_SECONDARY)
        screen.blit(time_text, (x + self.padding + author_text.get_width() + 10, current_y))
        
        # Sentiment indicator
        sentiment_color = {
            'LEFT': colors.PRIMARY,  # Twitter Blue for left
            'RIGHT': colors.LIKE_RED,  # Red for right
            'NEUTRAL': colors.TEXT_SECONDARY  # Gray for neutral
        }[self.post.sentiment.name]
        sentiment_text = self.fonts['small'].render(f"• {self.post.sentiment.name}", True, sentiment_color)
        screen.blit(sentiment_text, (x + self.width - self.padding - sentiment_text.get_width(), current_y))
        
        current_y += 30
        
        # Content with text wrapping
        content_width = self.width - (self.padding * 2)
        words = self.post.content.split()
        line = ""
        for word in words:
            test_line = line + word + " "
            test_surface = self.fonts['normal'].render(test_line, True, colors.TEXT_PRIMARY)
            if test_surface.get_width() > content_width:
                text_surface = self.fonts['normal'].render(line, True, colors.TEXT_PRIMARY)
                screen.blit(text_surface, (x + self.padding, current_y))
                current_y += 25
                line = word + " "
            else:
                line = test_line
        if line:
            text_surface = self.fonts['normal'].render(line, True, colors.TEXT_PRIMARY)
            screen.blit(text_surface, (x + self.padding, current_y))
            current_y += 25
            
        # Draw image if present
        if self.image:
            screen.blit(self.image, (x + self.padding, current_y))
            current_y += self.image.get_height() + self.padding
            
        # Follower impact stats
        current_y = y + self.height - 60
        follower_stats = self.fonts['small'].render(
            f"Followers: +{self.post.followers_gained} -{self.post.followers_lost}", 
            True, 
            colors.TEXT_SECONDARY
        )
        screen.blit(follower_stats, (x + self.padding, current_y))
            
        # Engagement metrics
        current_y = y + self.height - 30
        metrics_spacing = 100
        
        # Comments
        comments_text = self.fonts['small'].render(f"✎ {len(self.post.comments)}", True, colors.TEXT_SECONDARY)
        screen.blit(comments_text, (x + self.padding, current_y))
        
        # Retweets
        retweets_text = self.fonts['small'].render(f"↺ {self.post.shares}", True, colors.RETWEET_GREEN)
        screen.blit(retweets_text, (x + self.padding + metrics_spacing, current_y))
        
        # Likes
        likes_text = self.fonts['small'].render(f"♥ {self.post.likes}", True, colors.LIKE_RED)
        screen.blit(likes_text, (x + self.padding + metrics_spacing * 2, current_y))
        
        return post_rect

class Comment:
    def __init__(self, comment_data, fonts, width=500):
        self.comment = comment_data
        self.fonts = fonts
        self.width = width
        self.height = 80
        
    def draw(self, screen, x, y):
        # Comment container
        comment_rect = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(screen, colors.BG_HOVER, comment_rect, border_radius=10)
        
        # Author
        author_text = self.fonts['normal'].render(f"@{self.comment.author}", True, colors.PRIMARY)
        screen.blit(author_text, (x + 15, y + 10))
        
        # Content
        content_text = self.fonts['normal'].render(self.comment.content, True, colors.TEXT_PRIMARY)
        screen.blit(content_text, (x + 15, y + 40))
        
        return comment_rect 
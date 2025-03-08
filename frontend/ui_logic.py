import pygame
import os
from .views.main_view import MainView
from src.game.game_manager import GameManager

class UILogic:
    def __init__(self, mediator):

        #mediator
        self.mediator = mediator
        self.mediator.set_ui_logic(self)

        pygame.init()
        pygame.font.init()
        
        #ui creation
        self.view = MainView(1200, 800)
        self.clock = pygame.time.Clock()


        #game manager instance
        self.game_manager = GameManager(self.mediator) 
        
        # Create uploads directory if it doesn't exist
        self.uploads_dir = "uploads"
        if not os.path.exists(self.uploads_dir):
            os.makedirs(self.uploads_dir)


    def handle_mouse_wheel(self, event):
            scroll_amount = 40  # Increased from 20 for smoother scrolling
            
            if self.view.viewing_comments:
                # Scroll up (button 4) should show more content above (negative scroll)
                # Scroll down (button 5) should show more content below (positive scroll)
                if event.button == 4:  # Scroll up
                    self.view.comments_scroll_y += scroll_amount
                else:  # Scroll down
                    # Calculate max scroll based on number of comments
                    total_comments_height = len(self.view.current_post.comments) * 90
                    viewport_height = 500 - 200  # Modal height minus space for original post and padding
                    max_scroll = -(max(0, total_comments_height - viewport_height))
                    
                    # Apply scroll with limits
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
            _, back_button = self.view.draw(self.game_manager.user, self.view.posts)
            if back_button.collidepoint(pos):
                self.view.viewing_comments = False
                self.view.current_post = None
                
        elif self.view.composing:
            _, tweet_button, upload_button = self.view.draw(self.game_manager.user, self.view.posts)
            if tweet_button.collidepoint(pos) and self.view.compose_text:
                # Create post with image if one is selected
                if self.view.selected_image:
                    self.game_manager.handle_post_creation(self.view.compose_text, self.view.selected_image)
                else:
                    self.game_manager.handle_post_creation(self.view.compose_text)
                self.view.compose_text = ""
                self.view.selected_image = None
                self.view.image_preview = None
                self.view.composing = False
            elif upload_button.collidepoint(pos):
                self.handle_image_upload()
                
        else:
            post_rects, compose_button = self.view.draw(self.game_manager.user, self.view.posts)
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
                    self.game_manager.handle_post_creation(self.view.compose_text)
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
            self.game_manager.update_game_state()
            
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
            self.view.draw(self.game_manager.user, self.view.posts)
            pygame.display.flip()
            self.clock.tick(60)
            
        pygame.quit() 

    def show_notification(self, message: str):
        # Create a pop-up surface
        font = pygame.font.Font(None, 36)  # Use default font and size
        text_surface = font.render(message, True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(600, 400))  # Center the text

        # Create a pop-up background
        popup_width, popup_height = 400, 200
        popup_surface = pygame.Surface((popup_width, popup_height))  # Size of the pop-up
        popup_surface.fill((0, 0, 0))  # Black background
        popup_surface.set_alpha(200)  # Set transparency

        # Draw the border
        border_thickness = 5
        pygame.draw.rect(self.view.screen, (255, 255, 255), (400 - border_thickness, 300 - border_thickness, popup_width + 2 * border_thickness, popup_height + 2 * border_thickness))  # White border

        # Display the pop-up
        self.view.screen.blit(popup_surface, (400, 300))  # Position the pop-up
        self.view.screen.blit(text_surface, text_rect)  # Draw the text

        # Draw the "X" button
        x_button_rect = pygame.Rect(550, 310, 30, 30)  # Position and size of the "X" button
        pygame.draw.rect(self.view.screen, (255, 0, 0), x_button_rect)  # Red "X" button
        x_font = pygame.font.Font(None, 36)
        x_surface = x_font.render("X", True, (255, 255, 255))  # White "X"
        self.view.screen.blit(x_surface, (x_button_rect.x + 5, x_button_rect.y))  # Center the "X" in the button

        # Update the display
        pygame.display.flip()

        # Wait for user to close the pop-up
        self.wait_for_close(x_button_rect)

    def wait_for_close(self, x_button_rect):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if the "X" button was clicked
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if x_button_rect.collidepoint(mouse_pos):
                            waiting = False  # Close the pop-up on "X" button click
                    else:
                        waiting = False  # Close the pop-up on any key press 

    def handle_image_upload(self):
        try:
            import tkinter as tk
            from tkinter import filedialog
            from PIL import Image  # We'll use PIL to handle image conversion
            
            # Create and hide the root window
            root = tk.Tk()
            root.withdraw()
            
            # Open file dialog
            file_path = filedialog.askopenfilename(
                title="Select an image",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg *.jpeg"),
                    ("All image files", "*.png *.jpg *.jpeg *.gif *.bmp")
                ]
            )
            
            if file_path:
                # Get the original filename without extension
                filename = os.path.splitext(os.path.basename(file_path))[0]
                new_path = os.path.join(self.uploads_dir, f"{filename}.png")
                
                # Open and convert image to PNG
                with Image.open(file_path) as img:
                    # Convert to RGB if necessary (in case of RGBA or other formats)
                    if img.mode in ('RGBA', 'LA'):
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[-1])
                        img = background
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Save as PNG
                    img.save(new_path, 'PNG')
                
                # Update view with selected image
                self.view.selected_image = new_path
                self.view.image_preview = pygame.image.load(new_path)
                
        except ImportError:
            self.show_notification("Error: Please install Pillow library (pip install Pillow)")
        except Exception as e:
            self.show_notification(f"Error uploading image: {str(e)}") 

import pygame
from .views.main_view import MainView
from src.game.game_manager import GameManager

class UILogic:
    def __init__(self, mediator):

        #creates an instance of the mediator
        self.mediator = mediator
        self.mediator.set_ui_logic(self)

        pygame.init()
        pygame.font.init()
        
        #creates an instance of the main view
        self.view = MainView(1200, 800)
        self.clock = pygame.time.Clock()


        #instance of the game manager
        self.game_manager = GameManager(self.mediator) 


    def handle_mouse_wheel(self, event):
            scroll_amount = 40  # Scrolling speed
            
            if self.view.viewing_comments:
                # Scroll up (button 4) should show more content above (negative scroll)
                # Scroll down (button 5) should show more content below (positive scroll)
                if event.button == 4:  # Scroll up button
                    self.view.comments_scroll_y = min(0, self.view.comments_scroll_y + scroll_amount)
                else:  # Scrolls down

                    # Don't allow scrolling past the last comment
                    if len(self.view.current_post.comments) * 100 > 800:  # If comments exceed the view height
                        max_scroll = -(len(self.view.current_post.comments) * 100 - 700)  # Leave some space at bottom
                        self.view.comments_scroll_y = max(max_scroll, self.view.comments_scroll_y - scroll_amount)
            else:
                if event.button == 4:  # Scroll up button
                    self.view.scroll_y = min(0, self.view.scroll_y + scroll_amount)
                else:  # Scroll down
                    if len(self.view.posts) * 200 > 800:  # If posts exceeds view height
                        max_scroll = -(len(self.view.posts) * 200 - 700)  # Leave space at the bottom
                        self.view.scroll_y = max(max_scroll, self.view.scroll_y - scroll_amount)
                
    def handle_mouse_click(self, pos):
            if self.view.viewing_comments:
                _, back_button = self.view.draw(self.game_manager.user, self.view.posts)
                if back_button.collidepoint(pos):
                    self.view.viewing_comments = False
                    self.view.current_post = None
                    
            elif self.view.composing:
                _, tweet_button = self.view.draw(self.game_manager.user, self.view.posts)
                if tweet_button.collidepoint(pos) and self.view.compose_text:
                    self.game_manager.handle_post_creation(self.view.compose_text)
                    self.view.compose_text = ""
                    self.view.composing = False
                    
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
            self.game_manager.update_potential_followers()
            
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

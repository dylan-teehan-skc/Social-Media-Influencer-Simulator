from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTabWidget, QHBoxLayout
)
from PyQt6.QtCore import pyqtSlot

from src.views.user_profile_widget import UserProfileWidget
from src.views.create_post_widget import CreatePostWidget
from src.views.feed_widget import FeedWidget
from src.views.follower_list_widget import FollowerListWidget
from src.views.theme_switcher_widget import ThemeSwitcherWidget
from src.views.style_manager import StyleManager
from src.views.news_widget import NewsWidget

class SocialMediaMainWindow(QMainWindow):
    """Main window for the social media application"""
    
    def __init__(self, user=None):
        super().__init__()
        self.user = user
        self.user_controller = None
        self.post_controller = None
        
        # Initialize theme manager
        self.theme_manager = StyleManager.get_instance()
        
        self.init_ui()
        
    def set_user_controller(self, controller):
        """Set the user controller and pass it to child widgets."""
        self.user_controller = controller
        self.profile_widget.set_user_controller(controller)
        self.create_post_widget.set_user_controller(controller)
        self.news_widget.set_user_controller(controller)
        
    def set_post_controller(self, controller):
        """Set the post controller and pass it to child widgets."""
        self.post_controller = controller
        self.feed_widget.set_post_controller(controller)
        self.create_post_widget.set_post_controller(controller)
        
    def update_user_profile(self):
        """Update the UI to reflect changes in the user object."""
        # Update the user reference in the profile widget
        if hasattr(self, 'profile_widget'):
            self.profile_widget.update_user(self.user_controller.user)
            
        # Update window title to show verification status
        if hasattr(self.user_controller.user, 'get_handle'):
            self.setWindowTitle(f"Social Media Simulator - {self.user_controller.user.get_handle()}")
        else:
            self.setWindowTitle(f"Social Media Simulator - {self.user_controller.user.handle}")
            
        # Refresh the feed to show updated posts with verified status
        if hasattr(self, 'feed_widget'):
            self.feed_widget.update_feed()
        
        # Refresh follower list to show updated user handle
        if hasattr(self, 'followers_widget'):
            self.followers_widget.update_followers()
            
        # Update the news widget with the current user
        if hasattr(self, 'news_widget'):
            self.news_widget.update_user(self.user_controller.user)
        
    def init_ui(self):
        self.setWindowTitle("Social Media Simulator")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget and main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Add theme switcher at the top
        self.theme_switcher = ThemeSwitcherWidget()
        main_layout.addWidget(self.theme_switcher)
        
        # Create tab widget
        tabs = QTabWidget()
        
        # Profile tab
        profile_tab = QWidget()
        profile_layout = QVBoxLayout()
        self.profile_widget = UserProfileWidget(self.user)
        profile_layout.addWidget(self.profile_widget)
        profile_tab.setLayout(profile_layout)
        
        # Feed tab
        feed_tab = QWidget()
        feed_layout = QVBoxLayout()
        self.create_post_widget = CreatePostWidget(self.user)
        self.feed_widget = FeedWidget(self.user)
        feed_layout.addWidget(self.create_post_widget)
        feed_layout.addWidget(self.feed_widget)
        feed_tab.setLayout(feed_layout)
        
        # Followers tab
        followers_tab = QWidget()
        followers_layout = QVBoxLayout()
        self.followers_widget = FollowerListWidget(self.user)
        followers_layout.addWidget(self.followers_widget)
        followers_tab.setLayout(followers_layout)
        
        # News tab
        news_tab = QWidget()
        news_layout = QVBoxLayout()
        self.news_widget = NewsWidget(self.user)
        news_layout.addWidget(self.news_widget)
        news_tab.setLayout(news_layout)
        
        # Add tabs to tab widget
        tabs.addTab(profile_tab, "Profile")
        tabs.addTab(feed_tab, "Feed")
        tabs.addTab(followers_tab, "Followers")
        tabs.addTab(news_tab, "News")
        
        # Connect signals
        if self.user:
            self.user.post_created.connect(self.on_post_created)
            self.user.follower_added.connect(self.on_follower_added)
            self.user.follower_removed.connect(self.on_follower_removed)
        
        # Add tab widget to main layout
        main_layout.addWidget(tabs)
        
        # Set central widget
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Apply initial theme
        self.theme_manager.set_theme("light")
        
    @pyqtSlot(object)
    def on_post_created(self, post):
        self.feed_widget.update_feed()
        
    @pyqtSlot(object)
    def on_follower_added(self, follower):
        self.followers_widget.update_followers()
        self.profile_widget.update_follower_count()
        
    @pyqtSlot(object)
    def on_follower_removed(self, follower):
        self.followers_widget.update_followers()
        self.profile_widget.update_follower_count() 
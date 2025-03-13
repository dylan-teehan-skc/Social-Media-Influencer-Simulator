from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QPushButton, QHBoxLayout, QLabel
)
from src.views.post_widget import PostWidget

class FeedWidget(QWidget):
    """Widget to display a feed of posts"""
    
    def __init__(self, user=None, parent=None):
        super().__init__(parent)
        self.user = user
        self.post_controller = None
        self.post_widgets = []
        self.show_trending = False
        self.init_ui()
        
    def set_post_controller(self, controller):
        """Set the post controller and pass it to child widgets."""
        self.post_controller = controller
        # Update existing post widgets
        for post_widget in self.post_widgets:
            post_widget.set_post_controller(controller)
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Feed controls
        controls_layout = QHBoxLayout()
        feed_label = QLabel("Feed")
        feed_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        controls_layout.addWidget(feed_label)
        
        # Toggle button for trending/regular feed
        self.toggle_button = QPushButton("Show Trending")
        self.toggle_button.clicked.connect(self.toggle_feed_type)
        controls_layout.addWidget(self.toggle_button)
        
        # Refresh button
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.update_feed)
        controls_layout.addWidget(refresh_button)
        
        layout.addLayout(controls_layout)
        
        # Feed scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.feed_layout = QVBoxLayout(scroll_content)
        
        self.update_feed()
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        self.setLayout(layout)
    
    def toggle_feed_type(self):
        """Toggle between regular and trending feed."""
        self.show_trending = not self.show_trending
        if self.show_trending:
            self.toggle_button.setText("Show Regular Feed")
        else:
            self.toggle_button.setText("Show Trending")
        self.update_feed()
        
    def update_feed(self):
        """Update the feed with the latest posts."""
        # Clear existing posts
        self.post_widgets = []
        while self.feed_layout.count():
            item = self.feed_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        if not self.post_controller:
            return
            
        # Get posts based on feed type
        if self.show_trending and self.post_controller:
            posts = self.post_controller.get_trending_posts(limit=10)
        elif self.user:
            posts = reversed(self.user.posts)
        else:
            posts = []
            
        # Add posts to the feed
        for post in posts:
            post_widget = PostWidget(post)
            if self.post_controller:
                post_widget.set_post_controller(self.post_controller)
            self.post_widgets.append(post_widget)
            self.feed_layout.addWidget(post_widget)
            
        # Add stretch to push posts to the top
        self.feed_layout.addStretch() 
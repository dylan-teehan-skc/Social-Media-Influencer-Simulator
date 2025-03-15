from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QTextEdit, QFrame, QDialog, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor, QPainterPath, QBrush
from src.models.post import Sentiment
from src.views.style_manager import StyleManager
from src.views.user_profile_widget import get_base_profile_picture_path, create_circular_pixmap
import os

class PostWidget(QWidget):
    """Widget to display a single post"""
    
    def __init__(self, post=None, parent=None):
        super().__init__(parent)
        self.post = post
        self.post_controller = None
        self.theme_manager = StyleManager.get_instance()
        self.init_ui()
        
        # Connect to theme changes
        self.theme_manager.theme_changed.connect(self.on_theme_changed)
        
    def set_post_controller(self, controller):
        """Set the post controller."""
        self.post_controller = controller
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Post frame
        self.post_frame = QFrame()
        self.post_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.post_frame.setFrameShadow(QFrame.Shadow.Raised)
        post_layout = QVBoxLayout()
        post_layout.setSpacing(10)  # Add more spacing between elements
        post_layout.setContentsMargins(10, 10, 10, 10)  # Add padding inside the frame
        
        # Author and timestamp
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)  # Add spacing between avatar and author info
        
        # Author profile picture
        self.author_avatar = QLabel()
        self.author_avatar.setFixedSize(40, 40)
        self.author_avatar.setMinimumSize(40, 40)  # Ensure minimum size
        
        # Path to base profile picture
        base_profile_path = get_base_profile_picture_path()
        
        # Load the profile picture
        profile_pixmap = QPixmap()
        if self.post and self.post.author and hasattr(self.post.author, 'profile_picture_path') and self.post.author.profile_picture_path:
            profile_pixmap.load(self.post.author.profile_picture_path)
            if profile_pixmap.isNull():  # If loading fails, use base picture
                profile_pixmap.load(base_profile_path)
        else:
            # Use base profile picture
            profile_pixmap.load(base_profile_path)
        
        # Create and set circular avatar
        if not profile_pixmap.isNull():
            circular_pixmap = create_circular_pixmap(profile_pixmap, size=40, border_size=2)
            self.author_avatar.setPixmap(circular_pixmap)
        
        header_layout.addWidget(self.author_avatar)
        
        # Author info layout (name and timestamp)
        author_info_layout = QVBoxLayout()
        author_info_layout.setSpacing(2)  # Reduce spacing between handle and timestamp
        
        self.author_label = QLabel(f"@{self.post.author.handle}" if self.post.author else "Anonymous")
        self.author_label.setStyleSheet("font-weight: bold;")
        author_info_layout.addWidget(self.author_label)
        
        self.timestamp_label = QLabel(self.post.timestamp.strftime("%Y-%m-%d %H:%M"))
        self.timestamp_label.setStyleSheet("color: gray; font-size: 10px;")
        author_info_layout.addWidget(self.timestamp_label)
        
        header_layout.addLayout(author_info_layout, 1)  # Stretch factor 1
        
        # Post content
        content_label = QTextEdit()
        content_label.setReadOnly(True)
        if self.post:
            content_label.setText(self.post.content)
        else:
            content_label.setText("No content")
        content_label.setMaximumHeight(100)
        
        # Post image if available
        if self.post and self.post.image_path:
            self.image_label = QLabel()
            pixmap = QPixmap(self.post.image_path)
            scaled_pixmap = pixmap.scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label.setPixmap(scaled_pixmap)
            post_layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Post stats
        stats_layout = QHBoxLayout()
        
        # Likes
        likes_layout = QHBoxLayout()
        self.likes_icon = QLabel("❤️")
        likes_layout.addWidget(self.likes_icon)
        self.likes_label = QLabel(str(self.post.likes))
        likes_layout.addWidget(self.likes_label)
        stats_layout.addLayout(likes_layout)
        
        # Shares
        shares_layout = QHBoxLayout()
        self.shares_icon = QLabel("🔄")
        shares_layout.addWidget(self.shares_icon)
        self.shares_label = QLabel(str(self.post.shares))
        shares_layout.addWidget(self.shares_label)
        stats_layout.addLayout(shares_layout)
        
        # Comments
        comments_layout = QHBoxLayout()
        self.comments_icon = QLabel("💬")
        comments_layout.addWidget(self.comments_icon)
        self.comments_label = QLabel(str(len(self.post.comments)))
        comments_layout.addWidget(self.comments_label)
        stats_layout.addLayout(comments_layout)
        
        # Sentiment
        self.sentiment_label = QLabel()
        self.update_sentiment_label()  # Set initial value
        stats_layout.addWidget(self.sentiment_label, alignment=Qt.AlignmentFlag.AlignRight)
        
        # Add all layouts to post layout
        post_layout.addLayout(header_layout)
        post_layout.addWidget(content_label)
        post_layout.addLayout(stats_layout)
        
        self.post_frame.setLayout(post_layout)
        layout.addWidget(self.post_frame)
        self.setLayout(layout)
        
        # View comments button
        self.view_comments_button = QPushButton("View Comments")
        self.view_comments_button.clicked.connect(self.show_comments)
        layout.addWidget(self.view_comments_button)
        
        # Set up signals
        self.post.likes_changed.connect(self.update_likes)
        self.post.shares_changed.connect(self.update_shares)
        self.post.comments_changed.connect(self.update_comments)
        
        # Connect sentiment_changed signal if it exists
        if hasattr(self.post, 'sentiment_changed'):
            self.post.sentiment_changed.connect(lambda _: self.update_sentiment_label())
        
        # Apply theme-based styling
        self.update_theme_styling()
        
    def update_theme_styling(self):
        """Update styling based on current theme"""
        current_theme = self.theme_manager.current_theme
        
        if current_theme == "light":
            self.post_frame.setStyleSheet("""
                QFrame {
                    border: 1px solid #ccc;
                    border-radius: 8px;
                    background-color: white;
                    padding: 10px;
                }
            """)
        else:  # dark theme
            self.post_frame.setStyleSheet("""
                QFrame {
                    border: 1px solid #444;
                    border-radius: 8px;
                    background-color: #353535;
                    padding: 10px;
                }
            """)
        
    @pyqtSlot(str)
    def on_theme_changed(self, theme):
        """Handle theme changes"""
        self.update_theme_styling()
            
    @pyqtSlot()
    def like_post(self):
        if self.post and self.post_controller:
            self.post_controller.like_post(self.post)
            self.update_stats()
            
    @pyqtSlot()
    def share_post(self):
        if self.post and self.post_controller:
            self.post_controller.share_post(self.post)
            self.update_stats()
            
    @pyqtSlot()
    def comment_on_post(self):
        # This would normally open a dialog to enter a comment
        # For simplicity, we'll just add a default comment
        if self.post and self.post_controller:
            # Use the post controller to analyze the sentiment of the comment
            sentiment = self.post_controller.analyze_sentiment("Great post!")
            self.post_controller.comment_on_post(
                self.post, 
                "Great post!", 
                sentiment, 
                "user"
            )
            
    def update_stats(self):
        """Update the post statistics display."""
        if self.post:
            self.likes_label.setText(f"Likes: {self.post.likes}")
            self.shares_label.setText(f"Shares: {self.post.shares}") 

    def update_sentiment_label(self):
        """Update the sentiment label based on the post's sentiment."""
        if self.post.sentiment == Sentiment.LEFT:
            self.sentiment_label.setText("Left-leaning")
            self.sentiment_label.setStyleSheet("color: blue;")
        elif self.post.sentiment == Sentiment.RIGHT:
            self.sentiment_label.setText("Right-leaning")
            self.sentiment_label.setStyleSheet("color: red;")
        else:
            self.sentiment_label.setText("Neutral")
            self.sentiment_label.setStyleSheet("color: gray;")

    def show_comments(self):
        """Show the comments dialog with scrollable content."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Comments")
        dialog.setMinimumWidth(400)
        dialog.setMinimumHeight(500)  # Set a reasonable height
        
        layout = QVBoxLayout(dialog)
        
        # Create a scrollable area for comments
        from PyQt6.QtWidgets import QScrollArea
        
        # Container widget for all comments
        comments_container = QWidget()
        comments_layout = QVBoxLayout(comments_container)
        
        # Add comments to the container
        if self.post.comments:
            for comment in self.post.comments:
                comment_widget = self.create_comment_widget(comment)
                comments_layout.addWidget(comment_widget)
        else:
            # No comments message
            no_comments = QLabel("No comments yet")
            no_comments.setAlignment(Qt.AlignmentFlag.AlignCenter)
            comments_layout.addWidget(no_comments)
            
        # Add some spacing at the bottom
        comments_layout.addStretch()
        
        # Create scroll area and set properties
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(comments_container)
        
        layout.addWidget(scroll_area)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.accept)
        button_layout.addWidget(close_button)
        
        # Add button layout to main layout
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        dialog.exec()

    def create_comment_widget(self, comment):
        """Create a widget for a single comment"""
        comment_widget = QFrame()
        
        # Apply theme-appropriate styling
        if self.theme_manager.current_theme == "light":
            comment_widget.setStyleSheet("""
                QFrame {
                    border: 1px solid #eee;
                    border-radius: 4px;
                    background-color: #f9f9f9;
                    padding: 8px;
                    margin: 4px;
                }
            """)
        else:  # dark theme
            comment_widget.setStyleSheet("""
                QFrame {
                    border: 1px solid #444;
                    border-radius: 4px;
                    background-color: #2d2d2d;
                    padding: 8px;
                    margin: 4px;
                }
            """)
        
        comment_layout = QVBoxLayout(comment_widget)
        
        # Author and timestamp header
        header_layout = QHBoxLayout()
        
        # Author label with verified badge if applicable
        author_text = comment.author if isinstance(comment.author, str) else comment.author.handle
        author_label = QLabel(f"@{author_text}")
        author_label.setStyleSheet("font-weight: bold;")
        header_layout.addWidget(author_label)
        
        # Timestamp on the right
        timestamp_label = QLabel(comment.timestamp.strftime("%Y-%m-%d %H:%M"))
        timestamp_label.setStyleSheet("color: gray; font-size: 10px;")
        header_layout.addWidget(timestamp_label, alignment=Qt.AlignmentFlag.AlignRight)
        
        # Comment content
        content_label = QLabel(comment.content)
        content_label.setWordWrap(True)
        
        # Add widgets to layout
        comment_layout.addLayout(header_layout)
        comment_layout.addWidget(content_label)
        
        return comment_widget

    def update_likes(self, count):
        """Update the likes count label."""
        self.likes_label.setText(str(count))
        
    def update_shares(self, count):
        """Update the shares count label."""
        self.shares_label.setText(str(count))
        
    def update_comments(self, _):
        """Update the comments count label."""
        # Always get the current comments from the post
        self.comments_label.setText(str(len(self.post.comments))) 
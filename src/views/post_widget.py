from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QTextEdit, QFrame, QDialog, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QPixmap
from src.models.post import Sentiment

class PostWidget(QWidget):
    """Widget to display a single post"""
    
    def __init__(self, post=None, parent=None):
        super().__init__(parent)
        self.post = post
        self.post_controller = None
        self.init_ui()
        
    def set_post_controller(self, controller):
        """Set the post controller."""
        self.post_controller = controller
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Post frame
        post_frame = QFrame()
        post_frame.setFrameShape(QFrame.Shape.StyledPanel)
        post_frame.setFrameShadow(QFrame.Shadow.Raised)
        post_layout = QVBoxLayout()
        
        # Author and timestamp
        header_layout = QHBoxLayout()
        self.author_label = QLabel(f"@{self.post.author.handle}" if self.post.author else "Anonymous")
        self.author_label.setStyleSheet("font-weight: bold;")
        header_layout.addWidget(self.author_label)
        
        self.timestamp_label = QLabel(self.post.timestamp.strftime("%Y-%m-%d %H:%M"))
        self.timestamp_label.setStyleSheet("color: gray;")
        header_layout.addWidget(self.timestamp_label, alignment=Qt.AlignmentFlag.AlignRight)
        
        # Post content
        self.content_label = QLabel(self.post.content)
        self.content_label.setWordWrap(True)
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
        post_layout.addWidget(self.content_label)
        post_layout.addLayout(stats_layout)
        
        post_frame.setLayout(post_layout)
        layout.addWidget(post_frame)
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
        
        # Set border and background
        self.setStyleSheet("""
            QFrame {
                border: 1px solid #ccc;
                border-radius: 8px;
                background-color: white;
                padding: 10px;
            }
        """)
        
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
                comment_widget = QFrame()
                comment_widget.setStyleSheet("""
                    QFrame {
                        border: 1px solid #eee;
                        border-radius: 4px;
                        background-color: #f9f9f9;
                        padding: 8px;
                        margin: 4px;
                    }
                """)
                
                comment_layout = QVBoxLayout(comment_widget)
                
                # Author and timestamp
                header_layout = QHBoxLayout()
                author_label = QLabel(f"@{comment.author}")
                author_label.setStyleSheet("font-weight: bold;")
                header_layout.addWidget(author_label)
                
                timestamp_label = QLabel(comment.timestamp.strftime("%Y-%m-%d %H:%M"))
                timestamp_label.setStyleSheet("color: gray; font-size: 10px;")
                header_layout.addWidget(timestamp_label, alignment=Qt.AlignmentFlag.AlignRight)
                
                comment_layout.addLayout(header_layout)
                
                # Content
                content_label = QLabel(comment.content)
                content_label.setWordWrap(True)
                comment_layout.addWidget(content_label)
                
                comments_layout.addWidget(comment_widget)
        else:
            no_comments_label = QLabel("No comments yet.")
            no_comments_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            comments_layout.addWidget(no_comments_label)
        
        # Add stretch to push all comments to the top
        comments_layout.addStretch()
        
        # Create scroll area and add the comments container to it
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Important for proper resizing
        scroll_area.setWidget(comments_container)
        
        # Add scroll area to the main layout
        layout.addWidget(scroll_area)
        
        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)
        
        dialog.setLayout(layout)
        dialog.exec()

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
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QTextEdit, QMessageBox
)
from PyQt6.QtCore import pyqtSlot
from src.models.post import Sentiment

class CreatePostWidget(QWidget):
    """Widget to create a new post"""
    
    def __init__(self, user=None, parent=None):
        super().__init__(parent)
        self.user = user
        self.user_controller = None
        self.post_controller = None
        self.init_ui()
        
    def set_user_controller(self, controller):
        """Set the user controller."""
        self.user_controller = controller
        
    def set_post_controller(self, controller):
        """Set the post controller."""
        self.post_controller = controller
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Post content
        content_label = QLabel("What's on your mind?")
        self.content_edit = QTextEdit()
        
        # Image path
        image_layout = QHBoxLayout()
        image_label = QLabel("Image path (optional):")
        self.image_edit = QLineEdit()
        image_layout.addWidget(image_label)
        image_layout.addWidget(self.image_edit)
        
        # Post button
        self.post_button = QPushButton("Post")
        self.post_button.clicked.connect(self.create_post)
        
        # Add all widgets to layout
        layout.addWidget(content_label)
        layout.addWidget(self.content_edit)
        layout.addLayout(image_layout)
        layout.addWidget(self.post_button)
        
        self.setLayout(layout)
        
    @pyqtSlot()
    def create_post(self):
        """Create a new post."""
        content = self.content_edit.toPlainText().strip()
        if not content:
            return
            
        # Get the image path if an image was selected
        image_path = self.image_path if hasattr(self, 'image_path') else None
        
        # Create the post using the user controller, passing self as parent widget for warnings
        post = self.user_controller.create_post(content, image_path, parent_widget=self)
        
        # If post creation was cancelled or failed, return early
        if not post:
            return
            
        # Clear the content edit and image preview
        self.content_edit.clear()
        if hasattr(self, 'image_preview'):
            self.image_preview.clear()
        self.image_path = None
        
        QMessageBox.information(self, "Success", "Post created successfully!") 
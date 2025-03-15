from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QTextEdit, QMessageBox,
    QFileDialog
)
from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtGui import QPixmap, QIcon
from src.models.post import Sentiment

class CreatePostWidget(QWidget):
    """Widget to create a new post"""
    
    def __init__(self, user=None, parent=None):
        super().__init__(parent)
        self.user = user
        self.user_controller = None
        self.post_controller = None
        self.image_path = None
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
        content_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.content_edit = QTextEdit()
        self.content_edit.setPlaceholderText("Share your thoughts...")
        self.content_edit.setMinimumHeight(100)
        
        # Image upload
        image_layout = QHBoxLayout()
        image_label = QLabel("Upload image:")
        self.upload_button = QPushButton("⬆️ Select Image")  # Changed to upload arrow
        self.upload_button.clicked.connect(self.select_image)
        
        # Image preview label
        self.image_preview = QLabel("No image selected")
        self.image_preview.setFixedHeight(50)  # Fixed height for preview
        
        # Clear image button
        self.clear_image_button = QPushButton("❌ Clear Image")  # Keeping the clear icon
        self.clear_image_button.clicked.connect(self.clear_image)
        self.clear_image_button.setEnabled(False)  # Disabled until an image is selected
        
        # Add widgets to image layout
        image_layout.addWidget(image_label)
        image_layout.addWidget(self.upload_button)
        image_layout.addWidget(self.clear_image_button)
        
        # Post button
        self.post_button = QPushButton("Post")  # Removed the post icon
        self.post_button.clicked.connect(self.create_post)
        
        # Add all widgets to layout
        layout.addWidget(content_label)
        layout.addWidget(self.content_edit)
        layout.addLayout(image_layout)
        layout.addWidget(self.image_preview)
        layout.addWidget(self.post_button)
        
        self.setLayout(layout)
    
    def select_image(self):
        """Open file dialog to select an image"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.gif *.bmp)"
        )
        
        if file_path:
            self.image_path = file_path
            self.update_image_preview()
            self.clear_image_button.setEnabled(True)
    
    def update_image_preview(self):
        """Update the image preview label with the selected image"""
        if self.image_path:
            pixmap = QPixmap(self.image_path)
            scaled_pixmap = pixmap.scaledToHeight(50, Qt.TransformationMode.SmoothTransformation)
            self.image_preview.setPixmap(scaled_pixmap)
        else:
            self.image_preview.setText("No image selected")
    
    def clear_image(self):
        """Clear the selected image"""
        self.image_path = None
        self.image_preview.setText("No image selected")
        self.clear_image_button.setEnabled(False)
        
    @pyqtSlot()
    def create_post(self):
        """Create a new post."""
        content = self.content_edit.toPlainText().strip()
        if not content:
            return
            
        # Create the post using the user controller, passing self as parent widget for warnings
        post = self.user_controller.create_post(content, self.image_path, parent_widget=self)
        
        # If post creation was cancelled or failed, return early
        if not post:
            return
            
        # Clear the content edit and image preview
        self.content_edit.clear()
        self.clear_image()
        
        QMessageBox.information(self, "Success", "Post created successfully!") 
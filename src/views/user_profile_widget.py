from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QTextEdit, QMessageBox,
    QDialog, QDialogButtonBox, QFormLayout, QFrame,
    QFileDialog
)
from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtGui import QPixmap, QIcon, QFont, QPainter, QBrush, QPen, QColor, QPainterPath
from src.views.style_manager import StyleManager
import os
import shutil
from datetime import datetime

# Create the necessary directories for storing profile pictures and styles
def ensure_profile_directories():
    """Ensure the necessary directories exist for storing profile pictures"""
    # Get the views directory path
    views_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create user_data directory within views
    user_data_dir = os.path.join(views_dir, "user_data")
    os.makedirs(user_data_dir, exist_ok=True)
    
    # Create profile_pictures directory
    profile_pictures_dir = os.path.join(user_data_dir, "profile_pictures")
    os.makedirs(profile_pictures_dir, exist_ok=True)
    
    return profile_pictures_dir

# Get the path to the base profile picture
def get_base_profile_picture_path():
    """Get the path to the base profile picture"""
    views_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(views_dir, "user_data", "profile_pictures", "base_profile_picture.png")

# Ensure directories exist when module is imported
PROFILE_PICTURES_DIR = ensure_profile_directories()

# Function to create circular profile pictures
def create_circular_pixmap(pixmap, size=100, border_size=3, border_color="#888888"):
    """Create a circular cropped version of a pixmap with border"""
    # Handle null pixmap
    if pixmap.isNull():
        # Create a solid colored placeholder instead
        result = QPixmap(size, size)
        result.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(result)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw a filled circle
        painter.setPen(QPen(QColor(border_color), border_size))
        painter.setBrush(QBrush(QColor("#cccccc")))
        painter.drawEllipse(border_size//2, border_size//2, size - border_size, size - border_size)
        
        painter.end()
        return result
    
    # Scale the pixmap maintaining aspect ratio
    scaled_pixmap = pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    
    # Create a new transparent pixmap
    rounded = QPixmap(size, size)
    rounded.fill(Qt.GlobalColor.transparent)
    
    # Create a painter for drawing on the pixmap
    painter = QPainter(rounded)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    # Draw the scaled pixmap in a circular shape
    path = QPainterPath()
    path.addEllipse(border_size, border_size, size - 2*border_size, size - 2*border_size)
    painter.setClipPath(path)
    
    # Center the image if it's not square
    x_offset = (size - scaled_pixmap.width()) // 2
    y_offset = (size - scaled_pixmap.height()) // 2
    painter.drawPixmap(x_offset, y_offset, scaled_pixmap)
    
    # Reset clip path and draw border
    painter.setClipping(False)
    painter.setPen(QPen(QColor(border_color), border_size))
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.drawEllipse(border_size//2, border_size//2, size - border_size, size - border_size)
    
    painter.end()
    return rounded

class ProfileEditDialog(QDialog):
    """Dialog for editing profile information"""
    
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self.theme_manager = StyleManager.get_instance()
        self.temp_profile_picture_path = None  # Store the selected picture path
        self.init_ui()
        
        # Apply appropriate theme styling
        self.update_theme_styling()
        
        # Connect to theme changes
        self.theme_manager.theme_changed.connect(self.on_theme_changed)
        
    def init_ui(self):
        self.setWindowTitle("Edit Profile")
        self.setMinimumWidth(450)
        
        # Create form layout
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(20, 20, 20, 20)
        
        # Profile picture section
        picture_layout = QHBoxLayout()
        
        # Picture preview
        self.picture_preview = QLabel()
        self.picture_preview.setFixedSize(100, 100)
        
        # Path to base profile picture
        base_profile_path = get_base_profile_picture_path()
        
        # Set default or current profile picture
        if hasattr(self.user, 'profile_picture_path') and self.user.profile_picture_path:
            pixmap = QPixmap(self.user.profile_picture_path)
            self.temp_profile_picture_path = self.user.profile_picture_path
        else:
            # Use base profile picture
            pixmap = QPixmap(base_profile_path)
            self.temp_profile_picture_path = base_profile_path
        
        # Apply circular cropping
        circular_pixmap = create_circular_pixmap(pixmap, size=100)
        
        # Set the circular image
        self.picture_preview.setPixmap(circular_pixmap)
        
        # Picture buttons
        picture_buttons_layout = QVBoxLayout()
        
        # Upload button
        self.upload_button = QPushButton("Upload Picture")
        self.upload_button.clicked.connect(self.select_profile_picture)
        picture_buttons_layout.addWidget(self.upload_button)
        
        # Remove button
        self.remove_button = QPushButton("Remove Picture")
        self.remove_button.clicked.connect(self.remove_profile_picture)
        picture_buttons_layout.addWidget(self.remove_button)
        
        # Add to picture layout
        picture_layout.addWidget(self.picture_preview)
        picture_layout.addLayout(picture_buttons_layout)
        picture_layout.addStretch()
        
        # Add picture section to form
        form_layout.addRow("Profile Picture:", picture_layout)
        
        # User handle
        self.handle_edit = QLineEdit()
        if hasattr(self.user, 'get_handle'):
            self.handle_edit.setText(self.user.get_handle())
        else:
            self.handle_edit.setText(self.user.handle)
        self.handle_edit.setMinimumHeight(30)
        form_layout.addRow("Handle:", self.handle_edit)
        
        # User bio
        self.bio_edit = QTextEdit()
        if hasattr(self.user, 'get_bio'):
            self.bio_edit.setText(self.user.get_bio())
        else:
            self.bio_edit.setText(self.user.bio)
        self.bio_edit.setMinimumHeight(120)
        form_layout.addRow("Bio:", self.bio_edit)
        
        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        # Style the buttons
        save_button = button_box.button(QDialogButtonBox.StandardButton.Save)
        save_button.setMinimumHeight(35)
        save_button.setMinimumWidth(100)
        
        cancel_button = button_box.button(QDialogButtonBox.StandardButton.Cancel)
        cancel_button.setMinimumHeight(35)
        cancel_button.setMinimumWidth(100)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addSpacing(15)
        main_layout.addWidget(button_box, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(main_layout)
    
    def select_profile_picture(self):
        """Open file dialog to select a profile picture"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Profile Picture",
            "",
            "Image Files (*.png *.jpg *.jpeg *.gif *.bmp)"
        )
        
        if file_path:
            # Store the selected file path
            self.temp_profile_picture_path = file_path
            
            # Update preview with circular cropping
            pixmap = QPixmap(file_path)
            circular_pixmap = create_circular_pixmap(pixmap, size=100)
            
            # Set the circular image
            self.picture_preview.setPixmap(circular_pixmap)
    
    def remove_profile_picture(self):
        """Remove the custom profile picture and use the base profile picture"""
        # Path to base profile picture
        base_profile_path = get_base_profile_picture_path()
        
        # Use base profile picture
        self.temp_profile_picture_path = base_profile_path
        
        # Create circular preview
        pixmap = QPixmap(base_profile_path)
        circular_pixmap = create_circular_pixmap(pixmap, size=100)
        
        # Set the circular image
        self.picture_preview.setPixmap(circular_pixmap)
    
    def get_handle(self):
        """Get the entered handle"""
        return self.handle_edit.text()
    
    def get_bio(self):
        """Get the entered bio"""
        return self.bio_edit.toPlainText()
    
    def get_profile_picture_path(self):
        """Get the selected profile picture path"""
        return self.temp_profile_picture_path
    
    def save_profile_picture(self):
        """Save the profile picture to a permanent location if it's a new file"""
        if not self.temp_profile_picture_path:
            # Path to base profile picture
            base_profile_path = get_base_profile_picture_path()
            return base_profile_path
            
        # Path to base profile picture for comparison
        base_profile_path = get_base_profile_picture_path()
        
        # If it's the base profile picture, just return its path (don't copy it)
        if self.temp_profile_picture_path == base_profile_path:
            return base_profile_path
            
        # If it's already the user's profile picture, just return the path
        if hasattr(self.user, 'profile_picture_path') and self.temp_profile_picture_path == self.user.profile_picture_path:
            return self.temp_profile_picture_path
            
        # Generate a unique filename
        filename = f"profile_{self.user.handle}_{int(datetime.now().timestamp())}.png"
        dest_path = os.path.join(PROFILE_PICTURES_DIR, filename)
        
        # Copy the file to the destination with circular cropping
        try:
            # Create a circular cropped version of the image
            original_pixmap = QPixmap(self.temp_profile_picture_path)
            circular_pixmap = create_circular_pixmap(original_pixmap, size=200)
            
            # Save the circular image
            circular_pixmap.save(dest_path)
            return dest_path
        except Exception as e:
            print(f"Error saving profile picture: {e}")
            # Return base profile picture on error
            return base_profile_path
        
    def update_theme_styling(self):
        """Update styling based on current theme"""
        current_theme = self.theme_manager.current_theme
        
        if current_theme == "dark":
            self.setStyleSheet("""
                QDialog {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                }
                QLabel {
                    color: #e0e0e0;
                    font-size: 14px;
                }
                QLineEdit, QTextEdit {
                    background-color: #3d3d3d;
                    color: #e0e0e0;
                    border: 1px solid #555555;
                    border-radius: 4px;
                    padding: 5px;
                }
            """)
        else:
            self.setStyleSheet("""
                QDialog {
                    background-color: #ffffff;
                    color: #333333;
                }
                QLabel {
                    color: #333333;
                    font-size: 14px;
                }
                QLineEdit, QTextEdit {
                    background-color: #ffffff;
                    color: #333333;
                    border: 1px solid #e0dbd2;
                    border-radius: 4px;
                    padding: 5px;
                }
            """)
    
    @pyqtSlot(str)
    def on_theme_changed(self, theme):
        """Handle theme changes"""
        self.update_theme_styling()

class UserProfileWidget(QWidget):
    """Widget to display and edit user profile information"""
    
    def __init__(self, user=None, parent=None):
        super().__init__(parent)
        self.user = user
        self.user_controller = None
        self.theme_manager = StyleManager.get_instance()
        self.init_ui()
        
        # Connect to theme changes
        self.theme_manager.theme_changed.connect(self.on_theme_changed)
        
        # Connect to user signals if available
        if self.user:
            self.user.follower_added.connect(self.on_follower_added)
            self.user.follower_removed.connect(self.on_follower_removed)
            self.user.post_created.connect(self.on_post_created)
        
    def set_user_controller(self, controller):
        """Set the user controller."""
        self.user_controller = controller
        
    def update_user(self, user):
        """Update the widget with a new user object."""
        # Disconnect signals from old user if it exists
        if self.user:
            try:
                self.user.follower_added.disconnect(self.on_follower_added)
                self.user.follower_removed.disconnect(self.on_follower_removed)
                self.user.post_created.disconnect(self.on_post_created)
            except:
                # Ignore errors if signals were not connected
                pass
        
        # Update user reference
        self.user = user
        
        # Connect signals to new user
        if self.user:
            self.user.follower_added.connect(self.on_follower_added)
            self.user.follower_removed.connect(self.on_follower_removed)
            self.user.post_created.connect(self.on_post_created)
        
        # Update the displayed handle
        self.handle_label.setText(f"@{self.user.get_handle() if hasattr(self.user, 'get_handle') else self.user.handle}")
        
        # Update the displayed bio
        self.bio_text.setText(self.user.get_bio() if hasattr(self.user, 'get_bio') else self.user.bio)
        
        # Update profile picture
        self.update_profile_picture()
            
        # Update the follower count display
        self.update_follower_count()
        
        # Update the post count display
        self.update_post_count()
        
    def update_profile_picture(self):
        """Update the profile picture display"""
        # Path to base profile picture
        base_profile_path = get_base_profile_picture_path()
        
        if hasattr(self.user, 'profile_picture_path') and self.user.profile_picture_path:
            pixmap = QPixmap(self.user.profile_picture_path)
        else:
            # Use base profile picture
            pixmap = QPixmap(base_profile_path)
            
        # Apply circular cropping
        circular_pixmap = create_circular_pixmap(pixmap, size=100)
        
        # Set the circular image
        self.avatar_label.setPixmap(circular_pixmap)
    
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Profile header with title and edit button
        header_layout = QHBoxLayout()
        profile_title = QLabel("User Profile")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        profile_title.setFont(title_font)
        header_layout.addWidget(profile_title)
        
        # Edit profile button
        self.edit_button = QPushButton("Edit Profile")
        self.edit_button.setIcon(QIcon.fromTheme("document-edit"))
        self.edit_button.setMinimumHeight(30)
        self.edit_button.clicked.connect(self.open_edit_dialog)
        header_layout.addWidget(self.edit_button, alignment=Qt.AlignmentFlag.AlignRight)
        
        # Profile content section
        content_frame = QFrame()
        content_frame.setFrameShape(QFrame.Shape.StyledPanel)
        content_frame.setFrameShadow(QFrame.Shadow.Raised)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)
        
        # Profile info section with avatar
        profile_info_layout = QHBoxLayout()
        
        # Avatar placeholder
        avatar_layout = QVBoxLayout()
        self.avatar_label = QLabel()
        self.avatar_label.setFixedSize(100, 100)
        
        # Set initial profile picture
        self.update_profile_picture()
        
        avatar_layout.addWidget(self.avatar_label, alignment=Qt.AlignmentFlag.AlignCenter)
        avatar_layout.addWidget(QLabel("Profile Picture"), alignment=Qt.AlignmentFlag.AlignCenter)
        profile_info_layout.addLayout(avatar_layout)
        
        # User details
        user_details_layout = QVBoxLayout()
        user_details_layout.setSpacing(10)
        
        # Username section
        username_layout = QVBoxLayout()
        username_label = QLabel("Username")
        username_label.setStyleSheet("font-weight: bold; color: #666666;")
        username_layout.addWidget(username_label)
        
        self.handle_label = QLabel(f"@{self.user.handle if self.user else ''}")
        handle_font = QFont()
        handle_font.setPointSize(14)
        handle_font.setBold(True)
        self.handle_label.setFont(handle_font)
        username_layout.addWidget(self.handle_label)
        user_details_layout.addLayout(username_layout)
        
        # Bio section
        bio_layout = QVBoxLayout()
        bio_header = QLabel("Bio")
        bio_header.setStyleSheet("font-weight: bold; color: #666666;")
        bio_layout.addWidget(bio_header)
        
        self.bio_text = QLabel(self.user.bio if self.user else "")
        self.bio_text.setWordWrap(True)
        self.bio_text.setStyleSheet("padding: 10px; background-color: rgba(0, 0, 0, 0.05); border-radius: 5px;")
        bio_layout.addWidget(self.bio_text)
        user_details_layout.addLayout(bio_layout)
        
        # Add user details to profile info layout
        profile_info_layout.addLayout(user_details_layout)
        
        # Add profile info to content layout
        content_layout.addLayout(profile_info_layout)
        
        # Stats section
        stats_frame = QFrame()
        stats_frame.setFrameShape(QFrame.Shape.StyledPanel)
        stats_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 0.05);
                border-radius: 5px;
                padding: 5px;
            }
        """)
        stats_layout = QVBoxLayout(stats_frame)
        
        # Stats header
        stats_header = QLabel("Account Statistics")
        stats_header.setStyleSheet("font-weight: bold; font-size: 14px;")
        stats_layout.addWidget(stats_header)
        
        # Stats grid (for follower count and other future stats)
        stats_info_layout = QHBoxLayout()
        
        # Followers stat
        followers_layout = QVBoxLayout()
        followers_icon_label = QLabel("👥")
        followers_icon_label.setStyleSheet("font-size: 24px;")
        followers_layout.addWidget(followers_icon_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.follower_count = QLabel()
        self.update_follower_count()
        self.follower_count.setAlignment(Qt.AlignmentFlag.AlignCenter)
        followers_layout.addWidget(self.follower_count)
        
        stats_info_layout.addLayout(followers_layout)
        
        # Posts stat (placeholder for future)
        posts_layout = QVBoxLayout()
        posts_icon_label = QLabel("📝")
        posts_icon_label.setStyleSheet("font-size: 24px;")
        posts_layout.addWidget(posts_icon_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Create a dynamic post count label
        self.posts_count_label = QLabel()
        self.posts_count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        posts_layout.addWidget(self.posts_count_label)
        
        stats_info_layout.addLayout(posts_layout)
        
        # Add stats info to stats layout
        stats_layout.addLayout(stats_info_layout)
        
        # Add stats frame to content layout
        content_layout.addWidget(stats_frame)
        
        # Add layouts to main layout
        main_layout.addLayout(header_layout)
        main_layout.addWidget(content_frame)
        main_layout.addStretch()
        
        self.setLayout(main_layout)
        
        # Update the post count on initialization
        self.update_post_count()
        
        # Apply theme-specific styling
        self.update_theme_styling()
        
    @pyqtSlot()
    def open_edit_dialog(self):
        """Open dialog to edit profile details"""
        dialog = ProfileEditDialog(self.user, self)
        
        # If dialog is accepted (Save button clicked), update the profile
        if dialog.exec() == QDialog.DialogCode.Accepted and self.user_controller:
            # Save the profile picture if one was selected
            profile_picture_path = dialog.save_profile_picture()
            
            # Update user's profile in the controller
            updated_user = self.user_controller.update_profile(
                handle=dialog.get_handle(),
                bio=dialog.get_bio(),
                profile_picture_path=profile_picture_path
            )
            
            # Make sure our reference to the user is updated
            self.user = updated_user
            
            # Update the UI with the new user details
            self.handle_label.setText(f"@{self.user.get_handle() if hasattr(self.user, 'get_handle') else self.user.handle}")
            self.bio_text.setText(self.user.get_bio() if hasattr(self.user, 'get_bio') else self.user.bio)
            
            # Update the profile picture display
            self.update_profile_picture()
            
            # Get the main controller to update the main window
            from src.controllers.main_controller import MainController
            main_controller = MainController.get_instance()
            if main_controller and hasattr(main_controller, 'main_window'):
                main_controller.main_window.update_user_profile()
            
            QMessageBox.information(self, "Success", "Profile updated successfully!")
        
    def update_follower_count(self):
        """Update the follower count display."""
        if hasattr(self, 'follower_count') and self.user:
            count = self.user.follower_count
            
            # Add visual indicator if verified
            if hasattr(self.user, 'get_handle') and '✔️' in self.user.get_handle():
                self.follower_count.setText(f"{count} Followers\n(Verified Account ✔️)")
            else:
                self.follower_count.setText(f"{count} Followers")
    
    def update_post_count(self):
        """Update the post count display."""
        if hasattr(self, 'posts_count_label') and self.user:
            # Get the post count from the user's posts list
            post_count = len(self.user.posts) if hasattr(self.user, 'posts') else 0
            self.posts_count_label.setText(f"{post_count} Posts")
    
    def update_theme_styling(self):
        """Update styling based on current theme"""
        current_theme = self.theme_manager.current_theme
        
        if current_theme == "dark":
            self.bio_text.setStyleSheet("""
                padding: 10px; 
                background-color: rgba(255, 255, 255, 0.1); 
                border-radius: 5px;
                color: #e0e0e0;
            """)
        else:
            self.bio_text.setStyleSheet("""
                padding: 10px; 
                background-color: rgba(0, 0, 0, 0.05); 
                border-radius: 5px;
                color: #333333;
            """)
    
    @pyqtSlot(str)
    def on_theme_changed(self, theme):
        """Handle theme changes"""
        self.update_theme_styling()

    # Add signal handlers
    @pyqtSlot(object)
    def on_follower_added(self, follower):
        """Handle follower added signal"""
        self.update_follower_count()
        
    @pyqtSlot(object)
    def on_follower_removed(self, follower):
        """Handle follower removed signal"""
        self.update_follower_count()
        
    @pyqtSlot(object)
    def on_post_created(self, post):
        """Handle post created signal"""
        self.update_post_count() 
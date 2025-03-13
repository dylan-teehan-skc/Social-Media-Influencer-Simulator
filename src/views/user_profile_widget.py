from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QTextEdit, QMessageBox
)
from PyQt6.QtCore import pyqtSlot

class UserProfileWidget(QWidget):
    """Widget to display and edit user profile information"""
    
    def __init__(self, user=None, parent=None):
        super().__init__(parent)
        self.user = user
        self.user_controller = None
        self.init_ui()
        
    def set_user_controller(self, controller):
        """Set the user controller."""
        self.user_controller = controller
        
    def update_user(self, user):
        """Update the widget with a new user object."""
        self.user = user
        
        # Update the displayed handle
        if hasattr(self.user, 'get_handle'):
            self.handle_edit.setText(self.user.get_handle())
        else:
            self.handle_edit.setText(self.user.handle)
            
        # Update the displayed bio
        if hasattr(self.user, 'get_bio'):
            self.bio_edit.setText(self.user.get_bio())
        else:
            self.bio_edit.setText(self.user.bio)
            
        # Update the follower count display
        self.update_follower_count()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # User handle
        handle_layout = QHBoxLayout()
        handle_label = QLabel("Handle:")
        self.handle_edit = QLineEdit(self.user.handle if self.user else "")
        handle_layout.addWidget(handle_label)
        handle_layout.addWidget(self.handle_edit)
        
        # User bio
        bio_layout = QHBoxLayout()
        bio_label = QLabel("Bio:")
        self.bio_edit = QTextEdit()
        if self.user:
            self.bio_edit.setText(self.user.bio)
        self.bio_edit.setMaximumHeight(100)
        bio_layout.addWidget(bio_label)
        bio_layout.addWidget(self.bio_edit)
        
        # Follower count
        follower_layout = QHBoxLayout()
        follower_label = QLabel("Followers:")
        self.follower_count = QLabel(str(self.user.follower_count if self.user else 0))
        follower_layout.addWidget(follower_label)
        follower_layout.addWidget(self.follower_count)
        
        # Update profile button
        self.update_button = QPushButton("Update Profile")
        self.update_button.clicked.connect(self.update_profile)
        
        # Add all layouts to main layout
        layout.addLayout(handle_layout)
        layout.addLayout(bio_layout)
        layout.addLayout(follower_layout)
        layout.addWidget(self.update_button)
        layout.addStretch()
        
        self.setLayout(layout)
        
    @pyqtSlot()
    def update_profile(self):
        if self.user_controller:
            self.user_controller.update_profile(
                handle=self.handle_edit.text(),
                bio=self.bio_edit.toPlainText()
            )
            QMessageBox.information(self, "Success", "Profile updated successfully!")
        else:
            QMessageBox.warning(self, "Error", "User controller not set!")
        
    def update_follower_count(self):
        """Update the follower count display."""
        if hasattr(self, 'follower_count') and self.user:
            count = self.user.follower_count
            self.follower_count.setText(f"Followers: {count}")
            
            # Add visual indicator if verified
            if hasattr(self.user, 'get_handle') and '✔️' in self.user.get_handle():
                self.follower_count.setText(f"{count} (Verified Account)") 
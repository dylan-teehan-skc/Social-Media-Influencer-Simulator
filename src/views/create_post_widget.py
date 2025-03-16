from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.models.post import Sentiment
from src.patterns.decorator.sponsered_user import SponsoredUser


class CreatePostWidget(QWidget):
    """Widget to create a new post"""

    # Signal emitted when a post is created
    post_created = pyqtSignal()

    def __init__(self, user_controller=None, post_controller=None, user=None):
        """Initialize the create post widget."""
        super().__init__()
        self.user_controller = user_controller
        self.user = user
        self.post_controller = post_controller
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
        self.upload_button = QPushButton(
            "⬆️ Select Image"
        )  # Changed to upload arrow
        self.upload_button.clicked.connect(self.select_image)

        # Image preview label
        self.image_preview = QLabel("No image selected")
        self.image_preview.setFixedHeight(50)  # Fixed height for preview

        # Clear image button
        self.clear_image_button = QPushButton(
            "❌ Clear Image"
        )  # Keeping the clear icon
        self.clear_image_button.clicked.connect(self.clear_image)
        # Disabled until an image is selected
        self.clear_image_button.setEnabled(False)

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
            "Image Files (*.png *.jpg *.jpeg *.gif *.bmp)",
        )

        if file_path:
            self.image_path = file_path
            self.update_image_preview()
            self.clear_image_button.setEnabled(True)

    def update_image_preview(self):
        """Update the image preview label with the selected image"""
        if self.image_path:
            pixmap = QPixmap(self.image_path)
            scaled_pixmap = pixmap.scaledToHeight(
                50, Qt.TransformationMode.SmoothTransformation
            )
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
        """Create a new post with the current content and image."""
        content = self.content_edit.toPlainText().strip()

        if not content:
            QMessageBox.warning(
                self, "Empty Post", "Please enter some content for your post."
            )
            return

        # Create the post using the user_controller's create_post method
        if self.user_controller:
            # Create the post
            post = self.user_controller.create_post(
                content, self.image_path, parent_widget=self
            )

            # If post creation was cancelled or failed, return early
            if not post:
                return

            # Check if this post affects the user's sponsorship
            from src.services.company_service import CompanyService

            company_service = CompanyService.get_instance()

            # Store the original user for comparison
            original_user = self.user_controller.user
            was_sponsored = isinstance(
                original_user, SponsoredUser
            ) or hasattr(original_user, "company_name")

            # Process the post and check for sponsorship changes
            updated_user, message = company_service.on_post_created(
                self.user_controller.user, post
            )

            # Check if sponsorship was lost
            sponsorship_lost = was_sponsored and not (
                isinstance(updated_user, SponsoredUser)
                or hasattr(updated_user, "company_name")
            )

            # Always update the user controller's reference with the possibly
            # updated user
            self.user_controller.user = updated_user

            # Update the main controller's reference to the user
            from src.controllers.main_controller import MainController

            main_controller = MainController.get_instance()
            if main_controller:
                main_controller.user = updated_user

                # If the sponsorship was lost, show termination message before
                # updating UI
                if sponsorship_lost or (message and "terminated" in message):
                    QMessageBox.warning(
                        self,
                        "Sponsorship Terminated",
                        message
                        or "Your sponsorship has been terminated due to content that conflicts with your sponsor's values.",
                    )

                    # Force a complete refresh of the UI after sponsorship
                    # termination
                    if hasattr(main_controller, "main_window"):
                        # Update the user profile
                        main_controller.main_window.update_user_profile()

                        # Force a complete refresh of the news tab
                        if hasattr(main_controller.main_window, "news_widget"):
                            main_controller.main_window.news_widget.user = (
                                updated_user
                            )
                            main_controller.main_window.news_widget.update_sponsorship_status()
                            main_controller.main_window.news_widget.update()
                            main_controller.main_window.news_widget.repaint()

                        # Force a complete repaint of the main window
                        main_controller.main_window.update()
                        main_controller.main_window.repaint()

                        # Try to force Qt to process events
                        from PyQt6.QtCore import QCoreApplication

                        QCoreApplication.processEvents()

                # For non-termination cases, just update normally
                elif hasattr(main_controller, "main_window"):
                    # Update the user profile
                    main_controller.main_window.update_user_profile()

                    # Always update the news tab to reflect any sponsorship
                    # changes
                    if hasattr(main_controller.main_window, "news_widget"):
                        main_controller.main_window.news_widget.update_user(
                            updated_user
                        )
                        main_controller.main_window.news_widget.update()

                    # Show warning message if there is one but sponsorship
                    # wasn't terminated
                    if message and "Warning" in message:
                        QMessageBox.warning(
                            self, "Sponsorship Warning", message
                        )

            # Clear the form
            self.content_edit.clear()
            self.clear_image()

            # Show success message
            QMessageBox.information(
                self, "Success", "Post created successfully!"
            )
        else:
            QMessageBox.warning(
                self,
                "Error",
                "Could not create post - user controller not set.",
            )

    def get_selected_sentiment(self):
        """Get the sentiment for the post based on content analysis.

        In a real application, this would use NLP to analyze the content.
        For this simulation, we'll randomly select a sentiment with a bias
        toward neutral.
        """
        import random

        # For testing sponsorship termination, we'll increase the likelihood
        # of getting LEFT or RIGHT sentiments
        sentiments = [
            Sentiment.LEFT,
            Sentiment.LEFT,  # Increased weight for LEFT
            Sentiment.RIGHT,
            Sentiment.RIGHT,  # Increased weight for RIGHT
            Sentiment.NEUTRAL,
        ]

        return random.choice(sentiments)

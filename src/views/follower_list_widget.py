from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.models.post import Sentiment
from src.views.style_manager import StyleManager


class FollowerListDialog(QDialog):
    """Dialog to display a scrollable list of followers"""

    def __init__(self, followers, parent=None):
        super().__init__(parent)
        self.followers = followers
        self.theme_manager = StyleManager.get_instance()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Followers List")
        self.setMinimumWidth(400)
        self.setMinimumHeight(500)

        layout = QVBoxLayout(self)

        # Create a scrollable area for followers
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Container widget for all followers
        container = QWidget()
        followers_layout = QVBoxLayout(container)

        # Add followers to the container
        if self.followers:
            for follower in self.followers:
                follower_widget = self.create_follower_widget(follower)
                followers_layout.addWidget(follower_widget)
        else:
            # No followers message
            no_followers = QLabel("No followers yet")
            no_followers.setAlignment(Qt.AlignmentFlag.AlignCenter)
            followers_layout.addWidget(no_followers)

        # Add some spacing at the bottom
        followers_layout.addStretch()

        scroll_area.setWidget(container)
        layout.addWidget(scroll_area)

        # Close button
        button_layout = QHBoxLayout()
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(
            close_button, alignment=Qt.AlignmentFlag.AlignCenter
        )

        layout.addLayout(button_layout)

    def create_follower_widget(self, follower):
        """Create a widget for displaying a follower"""
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)

        # Apply theme-appropriate styling
        if self.theme_manager.current_theme == "light":
            frame.setStyleSheet(
                """
                QFrame {
                    border: 1px solid #e0e0e0;
                    border-radius: 4px;
                    background-color: #f9f9f9;
                    padding: 10px;
                    margin: 4px;
                }
            """
            )
        else:  # dark theme
            frame.setStyleSheet(
                """
                QFrame {
                    border: 1px solid #444;
                    border-radius: 4px;
                    background-color: #2d2d2d;
                    padding: 10px;
                    margin: 4px;
                }
            """
            )

        layout = QHBoxLayout(frame)

        # Follower handle
        handle_label = QLabel(f"@{follower.handle}")
        handle_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(handle_label)

        # Sentiment indicator
        sentiment_text = ""
        sentiment_color = ""

        if follower.sentiment == Sentiment.LEFT:
            sentiment_text = "Left-leaning"
            sentiment_color = "#3498db"  # Blue
        elif follower.sentiment == Sentiment.RIGHT:
            sentiment_text = "Right-leaning"
            sentiment_color = "#e74c3c"  # Red
        else:
            sentiment_text = "Neutral"
            sentiment_color = "#95a5a6"  # Gray

        sentiment_label = QLabel(sentiment_text)
        sentiment_label.setStyleSheet(f"color: {sentiment_color};")
        layout.addWidget(
            sentiment_label, alignment=Qt.AlignmentFlag.AlignRight
        )

        return frame


class FollowerListWidget(QWidget):
    """Widget for displaying follower sentiment breakdown."""

    def __init__(self, user):
        """Initialize with a user object."""
        super().__init__()
        self.user = user  # Store the user directly, not a controller
        self.init_ui()

        # Connect to signals
        self.user.follower_added.connect(self.update_followers)
        self.user.follower_removed.connect(self.update_followers)

    def init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)

        # Title
        title = QLabel("Follower Sentiment Breakdown")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        # Create sentiment breakdown widgets
        self.left_frame = self.create_sentiment_frame(
            "Left-leaning", "#3498db"
        )  # Blue
        self.neutral_frame = self.create_sentiment_frame(
            "Neutral", "#95a5a6"
        )  # Gray
        self.right_frame = self.create_sentiment_frame(
            "Right-leaning", "#e74c3c"
        )  # Red

        layout.addWidget(self.left_frame)
        layout.addWidget(self.neutral_frame)
        layout.addWidget(self.right_frame)

        # Total followers count
        self.total_label = QLabel("Total Followers: 0")
        self.total_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(self.total_label)

        # View Followers button
        self.view_followers_button = QPushButton("View Followers")
        self.view_followers_button.clicked.connect(self.show_followers_dialog)
        layout.addWidget(
            self.view_followers_button, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Add stretch to push everything to the top
        layout.addStretch()

        # Update the stats
        self.update_followers()

    def show_followers_dialog(self):
        """Show dialog with scrollable list of followers"""
        dialog = FollowerListDialog(self.user.followers, self)
        dialog.exec()

    def create_sentiment_frame(self, title, color):
        """Create a frame for displaying sentiment statistics."""
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setStyleSheet(
            f"border: 1px solid {color}; border-radius: 5px; padding: 5px;"
        )

        layout = QVBoxLayout(frame)

        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {color}; font-weight: bold;")
        layout.addWidget(title_label)

        # Progress bar
        progress_bar = QProgressBar()
        progress_bar.setRange(0, 100)
        progress_bar.setValue(0)
        progress_bar.setTextVisible(True)
        progress_bar.setStyleSheet(
            f"QProgressBar {{ border: 1px solid {color}; border-radius: 3px; text-align: center; }} "
            f"QProgressBar::chunk {{ background-color: {color}; }}"
        )
        layout.addWidget(progress_bar)

        # Count label
        count_label = QLabel("0 followers (0%)")
        layout.addWidget(count_label)

        # Store references to widgets
        frame.progress_bar = progress_bar
        frame.count_label = count_label

        return frame

    def update_followers(self):
        """Update the follower statistics."""
        # Get all followers directly from the user
        followers = self.user.followers
        total_followers = len(followers)

        # Count followers by sentiment
        left_count = sum(1 for f in followers if f.sentiment == Sentiment.LEFT)
        right_count = sum(
            1 for f in followers if f.sentiment == Sentiment.RIGHT
        )
        neutral_count = sum(
            1 for f in followers if f.sentiment == Sentiment.NEUTRAL
        )

        # Calculate percentages
        left_percent = (
            (left_count / total_followers * 100) if total_followers > 0 else 0
        )
        right_percent = (
            (right_count / total_followers * 100) if total_followers > 0 else 0
        )
        neutral_percent = (
            (neutral_count / total_followers * 100)
            if total_followers > 0
            else 0
        )

        # Update the UI
        self.left_frame.progress_bar.setValue(int(left_percent))
        self.left_frame.count_label.setText(
            f"{left_count} followers ({left_percent:.1f}%)"
        )

        self.neutral_frame.progress_bar.setValue(int(neutral_percent))
        self.neutral_frame.count_label.setText(
            f"{neutral_count} followers ({neutral_percent:.1f}%)"
        )

        self.right_frame.progress_bar.setValue(int(right_percent))
        self.right_frame.count_label.setText(
            f"{right_count} followers ({right_percent:.1f}%)"
        )

        self.total_label.setText(f"Total Followers: {total_followers}")

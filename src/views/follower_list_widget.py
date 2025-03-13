from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QFrame
from PyQt6.QtCore import Qt
from src.models.post import Sentiment

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
        self.left_frame = self.create_sentiment_frame("Left-leaning", "#3498db")  # Blue
        self.neutral_frame = self.create_sentiment_frame("Neutral", "#95a5a6")    # Gray
        self.right_frame = self.create_sentiment_frame("Right-leaning", "#e74c3c") # Red
        
        layout.addWidget(self.left_frame)
        layout.addWidget(self.neutral_frame)
        layout.addWidget(self.right_frame)
        
        # Total followers count
        self.total_label = QLabel("Total Followers: 0")
        self.total_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(self.total_label)
        
        # Add stretch to push everything to the top
        layout.addStretch()
        
        # Update the stats
        self.update_followers()
        
    def create_sentiment_frame(self, title, color):
        """Create a frame for displaying sentiment statistics."""
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setStyleSheet(f"border: 1px solid {color}; border-radius: 5px; padding: 5px;")
        
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
        progress_bar.setStyleSheet(f"QProgressBar {{ border: 1px solid {color}; border-radius: 3px; text-align: center; }} "
                                  f"QProgressBar::chunk {{ background-color: {color}; }}")
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
        right_count = sum(1 for f in followers if f.sentiment == Sentiment.RIGHT)
        neutral_count = sum(1 for f in followers if f.sentiment == Sentiment.NEUTRAL)
        
        # Calculate percentages
        left_percent = (left_count / total_followers * 100) if total_followers > 0 else 0
        right_percent = (right_count / total_followers * 100) if total_followers > 0 else 0
        neutral_percent = (neutral_count / total_followers * 100) if total_followers > 0 else 0
        
        # Update the UI
        self.left_frame.progress_bar.setValue(int(left_percent))
        self.left_frame.count_label.setText(f"{left_count} followers ({left_percent:.1f}%)")
        
        self.neutral_frame.progress_bar.setValue(int(neutral_percent))
        self.neutral_frame.count_label.setText(f"{neutral_count} followers ({neutral_percent:.1f}%)")
        
        self.right_frame.progress_bar.setValue(int(right_percent))
        self.right_frame.count_label.setText(f"{right_count} followers ({right_percent:.1f}%)")
        
        self.total_label.setText(f"Total Followers: {total_followers}") 
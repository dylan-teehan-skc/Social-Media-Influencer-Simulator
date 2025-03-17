from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.views.post_widget import PostWidget


class FeedWidget(QWidget):

    def __init__(self, user=None, parent=None):
        super().__init__(parent)
        self.user = user
        self.post_controller = None
        self.post_widgets = []
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

        # Get user posts
        if self.user:
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

from datetime import datetime

from PyQt6.QtCore import QObject, QTimer


class AppController(QObject):
    """Main application controller that coordinates other controllers."""

    def __init__(self, user_controller, post_controller, follower_controller):
        """Initialize the app controller with other controllers."""
        super().__init__()
        self._user_controller = user_controller
        self._post_controller = post_controller
        self._follower_controller = follower_controller

        # Set up timer for periodic updates
        self._timer = QTimer()
        self._timer.timeout.connect(self._update_state)
        self._timer.start(1000)  # Update every second

        # Track last reputation update
        self._last_reputation_update = datetime.now().timestamp() * 1000

    def start(self):
        """Start the application."""
        # Initialize controllers
        self._user_controller.initialize()
        self._post_controller.initialize()
        self._follower_controller.initialize()

    def shutdown(self):
        """Shutdown the application."""
        self._timer.stop()

    def _update_state(self):
        """Update application state periodically."""
        current_time = datetime.now().timestamp() * 1000

        # Update reputation every 30 seconds
        if current_time - self._last_reputation_update >= 30000:
            self._user_controller.update_reputation(current_time)
            self._last_reputation_update = current_time

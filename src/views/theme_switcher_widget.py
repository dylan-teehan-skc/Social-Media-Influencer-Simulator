from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QSlider, QWidget

from src.views.style_manager import StyleManager


class ThemeSwitcherWidget(QWidget):
    """Widget for switching between dark and light themes using a slider"""

    def __init__(self):
        super().__init__()
        self.theme_manager = StyleManager.get_instance()
        self.init_ui()

        # Connect to theme changes
        self.theme_manager.theme_changed.connect(self.on_theme_changed)

    def init_ui(self):
        """Initialize the UI"""
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Add stretch to push widgets to the right
        layout.addStretch()

        # Create dark mode icon/label
        self.dark_icon = QLabel("🌙")  # Moon emoji for dark mode
        self.dark_icon.setToolTip("Dark Mode")
        layout.addWidget(self.dark_icon)

        # Create theme toggle slider
        self.theme_slider = QSlider(Qt.Orientation.Horizontal)
        self.theme_slider.setFixedWidth(40)  # Make slider small and compact
        self.theme_slider.setRange(0, 1)
        self.theme_slider.setPageStep(1)

        # Set initial slider position based on current theme
        self.update_slider_position()

        # Connect slider value changed signal
        self.theme_slider.valueChanged.connect(self.on_slider_value_changed)
        layout.addWidget(self.theme_slider)

        # Create light mode icon/label
        self.light_icon = QLabel("☀️")  # Sun emoji for light mode
        self.light_icon.setToolTip("Light Mode")
        layout.addWidget(self.light_icon)

        self.setLayout(layout)

    def update_slider_position(self):
        """Update slider position based on current theme"""
        if self.theme_manager.current_theme == "light":
            self.theme_slider.setValue(1)
        else:
            self.theme_slider.setValue(0)

    def on_slider_value_changed(self, value):
        """Handle slider value changes"""
        if value == 0 and self.theme_manager.current_theme != "dark":
            self.theme_manager.set_theme("dark")
        elif value == 1 and self.theme_manager.current_theme != "light":
            self.theme_manager.set_theme("light")

    @pyqtSlot(str)
    def on_theme_changed(self, theme):
        """Handle theme changes from external sources"""
        self.update_slider_position()

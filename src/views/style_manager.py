"""
Style manager for handling application themes and styling.
This module handles light and dark theme management within the views directory.
"""

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication
import os


class StyleManager(QObject):
    """Manages application themes (dark/light mode)"""
    
    # Signal emitted when theme changes
    theme_changed = pyqtSignal(str)
    
    # Singleton instance
    _instance = None
    
    @classmethod
    def get_instance(cls):
        """Get the singleton instance of StyleManager"""
        if cls._instance is None:
            cls._instance = StyleManager()
        return cls._instance
    
    def __init__(self):
        """Initialize the style manager"""
        super().__init__()
        self._current_theme = "light"  # Default theme
        
        # Create necessary directories
        self._ensure_style_directories()
        
    def _ensure_style_directories(self):
        """Ensure necessary directories exist for storing styles"""
        # Get the views directory path
        views_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Create user_data directory within views if it doesn't exist already
        user_data_dir = os.path.join(views_dir, "user_data")
        os.makedirs(user_data_dir, exist_ok=True)
        
    @property
    def current_theme(self):
        """Get the current theme"""
        return self._current_theme
    
    def toggle_theme(self):
        """Toggle between dark and light themes"""
        if self._current_theme == "light":
            self.set_theme("dark")
        else:
            self.set_theme("light")
    
    def set_theme(self, theme):
        """Set the application theme"""
        if theme not in ["light", "dark"]:
            raise ValueError("Theme must be 'light' or 'dark'")
            
        self._current_theme = theme
        
        # Apply the appropriate stylesheet
        if theme == "light":
            self._apply_light_theme()
        else:
            self._apply_dark_theme()
            
        # Emit signal that theme has changed
        self.theme_changed.emit(theme)
    
    def _apply_light_theme(self):
        """Apply light theme stylesheet"""
        light_stylesheet = """
        QMainWindow, QWidget {
            background-color: #f9f9f9;
            color: #333333;
        }
        
        QTabWidget::pane {
            border: 1px solid #e0e0e0;
            background-color: #ffffff;
        }
        
        QTabBar::tab {
            background-color: #f0f0f0;
            border: 1px solid #e0e0e0;
            padding: 8px 12px;
            margin-right: 2px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        
        QTabBar::tab:selected {
            background-color: #ffffff;
            border-bottom-color: #ffffff;
            font-weight: bold;
        }
        
        QPushButton {
            background-color: #4a86e8;
            color: white;
            border: none;
            padding: 6px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        
        QPushButton:hover {
            background-color: #3a76d8;
        }
        
        QPushButton:pressed {
            background-color: #2a66c8;
        }
        
        QLineEdit, QTextEdit {
            background-color: white;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            padding: 5px;
        }
        
        QProgressBar {
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            text-align: center;
            height: 12px;
        }
        
        QProgressBar::chunk {
            background-color: #4a86e8;
            border-radius: 3px;
        }

        QFrame {
            border: 1px solid #e0e0e0;
            border-radius: 4px;
        }
        
        QLabel {
            color: #333333;
        }
        
        QScrollArea {
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            background-color: #ffffff;
        }
        
        QScrollBar:vertical {
            border: none;
            background: #f0f0f0;
            width: 10px;
            border-radius: 5px;
        }

        QScrollBar::handle:vertical {
            background: #c0c0c0;
            min-height: 20px;
            border-radius: 5px;
        }

        QScrollBar::handle:vertical:hover {
            background: #a0a0a0;
        }
        """
        QApplication.instance().setStyleSheet(light_stylesheet)
    
    def _apply_dark_theme(self):
        """Apply dark theme stylesheet"""
        dark_stylesheet = """
        QMainWindow, QWidget {
            background-color: #2d2d2d;
            color: #e0e0e0;
        }
        
        QTabWidget::pane {
            border: 1px solid #444444;
            background-color: #353535;
        }
        
        QTabBar::tab {
            background-color: #444444;
            border: 1px solid #555555;
            padding: 5px 10px;
            margin-right: 2px;
        }
        
        QTabBar::tab:selected {
            background-color: #353535;
            border-bottom-color: #353535;
        }
        
        QPushButton {
            background-color: #0d8aee;
            color: white;
            border: none;
            padding: 5px 15px;
            border-radius: 3px;
        }
        
        QPushButton:hover {
            background-color: #2196F3;
        }
        
        QPushButton:pressed {
            background-color: #0c7cd5;
        }
        
        QLineEdit, QTextEdit {
            background-color: #424242;
            border: 1px solid #555555;
            border-radius: 3px;
            padding: 3px;
            color: #e0e0e0;
        }
        
        QProgressBar {
            border: 1px solid #555555;
            border-radius: 3px;
            text-align: center;
        }
        
        QProgressBar::chunk {
            background-color: #0d8aee;
        }
        """
        QApplication.instance().setStyleSheet(dark_stylesheet) 
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QScrollArea, QFrame, QMessageBox, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QFont, QColor
from src.services.company_service import CompanyService
from src.patterns.decorator.verified_user import VerifiedUser
from src.patterns.decorator.sponsered_user import SponsoredUser
from src.views.style_manager import StyleManager


class NewsWidget(QWidget):
    """Widget to display news and sponsorship opportunities"""
    
    def __init__(self, user=None, parent=None):
        super().__init__(parent)
        self.user = user
        self.user_controller = None
        self.theme_manager = StyleManager.get_instance()
        self.company_service = CompanyService.get_instance()
        self.init_ui()
        
        # Connect to theme changes
        self.theme_manager.theme_changed.connect(self.on_theme_changed)
        
    def set_user_controller(self, controller):
        """Set the user controller"""
        self.user_controller = controller
        
    def update_user(self, user):
        """Update the widget with a new user object"""
        # Update the user reference
        self.user = user
        
        # Force clear any cached state
        self.update()
        
        # Update the UI components
        self.update_sponsorship_status()
        self.refresh_companies_list()
        
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout()
        
        # Main title
        title_label = QLabel("News & Sponsorships")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Current sponsorship status
        self.sponsorship_frame = QFrame()
        self.sponsorship_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.sponsorship_frame.setFrameShadow(QFrame.Shadow.Raised)
        
        sponsorship_layout = QVBoxLayout(self.sponsorship_frame)
        
        self.status_label = QLabel()
        sponsorship_layout.addWidget(self.status_label)
        
        # Terminate sponsorship button (hidden by default)
        self.terminate_button = QPushButton("Terminate Sponsorship")
        self.terminate_button.clicked.connect(self.terminate_sponsorship)
        self.terminate_button.hide()
        sponsorship_layout.addWidget(self.terminate_button)
        
        layout.addWidget(self.sponsorship_frame)
        
        # Companies section
        companies_title = QLabel("Sponsorship Opportunities")
        companies_title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(companies_title)
        

        # Companies scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.companies_container = QWidget()
        self.companies_layout = QVBoxLayout(self.companies_container)
        
        scroll.setWidget(self.companies_container)
        layout.addWidget(scroll)
        
        self.setLayout(layout)
        
        # Initialize companies list
        self.refresh_companies_list()
        
        # Update sponsorship status
        self.update_sponsorship_status()
        
        # Apply theme styling
        self.update_theme_styling()
    
    def refresh_companies_list(self):
        """Refresh the list of companies"""
        # Clear existing companies
        while self.companies_layout.count():
            item = self.companies_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        # Add companies
        for company in self.company_service.companies:
            company_widget = self.create_company_widget(company)
            self.companies_layout.addWidget(company_widget)
        
        # Add stretch at the end
        self.companies_layout.addStretch()
    
    def create_company_widget(self, company):
        """Create a widget for displaying a company"""
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        
        # Base styling with clean design
        # We'll adapt colors based on theme in update_theme_styling
        self.update_company_frame_style(frame, company)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # Company name and alignment
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)
        
        # Company name (removed colored dot indicator)
        name_label = QLabel(company.name)
        name_label.setStyleSheet("font-weight: bold; font-size: 15px;")
        name_label.setProperty("company_name", True)  # Mark for theme styling
        header_layout.addWidget(name_label)
        
        # Political alignment tag
        alignment_label = QLabel(company.political_alignment_string)
        alignment_label.setStyleSheet("font-style: italic; padding: 4px 8px; border-radius: 10px;")
        
        if company.political_leaning.name == "LEFT":
            alignment_label.setStyleSheet(alignment_label.styleSheet() + "background-color: #d4e6f1; color: #2874a6;")
        elif company.political_leaning.name == "RIGHT":
            alignment_label.setStyleSheet(alignment_label.styleSheet() + "background-color: #f5b7b1; color: #a93226;")
        else:
            alignment_label.setStyleSheet(alignment_label.styleSheet() + "background-color: #eaeded; color: #5d6d7e;")
            
        header_layout.addWidget(alignment_label, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addLayout(header_layout)
        
        # Add a separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setProperty("separator", True)  # Mark for theme styling
        layout.addWidget(separator)
        
        # Company description
        desc_label = QLabel(company.description)
        desc_label.setWordWrap(True)
        desc_label.setProperty("description", True)  # Mark for theme styling
        layout.addWidget(desc_label)
        
        # Apply button
        apply_button = QPushButton("Apply for Sponsorship")
        apply_button.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Style the button according to the company's political leaning
        if company.political_leaning.name == "LEFT":
            apply_button.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    padding: 8px;
                    font-weight: bold;
                    border-radius: 8px;
                }
                QPushButton:hover { 
                    background-color: #2980b9; 
                }
                QPushButton:pressed { 
                    background-color: #1a5276; 
                }
            """)
        elif company.political_leaning.name == "RIGHT":
            apply_button.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    border: none;
                    padding: 8px;
                    font-weight: bold;
                    border-radius: 8px;
                }
                QPushButton:hover { 
                    background-color: #c0392b; 
                }
                QPushButton:pressed { 
                    background-color: #922b21; 
                }
            """)
        else:
            apply_button.setStyleSheet("""
                QPushButton {
                    background-color: #95a5a6;
                    color: white;
                    border: none;
                    padding: 8px;
                    font-weight: bold;
                    border-radius: 8px;
                }
                QPushButton:hover { 
                    background-color: #7f8c8d; 
                }
                QPushButton:pressed { 
                    background-color: #616a6b; 
                }
            """)
        
        apply_button.clicked.connect(lambda: self.apply_for_sponsorship(company))
        layout.addWidget(apply_button)
        
        # Store company reference for theme updates
        frame.setProperty("company", company.name)
        
        return frame
    
    def update_company_frame_style(self, frame, company=None):
        """Update the styling of company frames based on theme"""
        current_theme = self.theme_manager.current_theme
        
        if current_theme == "dark":
            frame.setStyleSheet("""
                QFrame {
                    border: 1px solid #444444;
                    border-radius: 12px;
                    background-color: #333333;
                    margin: 8px 4px;
                    padding: 0px;
                }
            """)
            
            # We need to use the fallback since shadow looks odd on dark theme
            frame.setStyleSheet("""
                QFrame {
                    border: 1px solid #444444;
                    border-radius: 12px;
                    background-color: #333333;
                    margin: 8px 4px;
                    padding: 0px;
                    border-bottom: 3px solid #444444;
                }
            """)
        else:
            frame.setStyleSheet("""
                QFrame {
                    border: 1px solid #dddddd;
                    border-radius: 12px;
                    background-color: white;
                    margin: 8px 4px;
                    padding: 0px;
                }
            """)
            
            # Add shadow effect using Qt's native shadow capabilities
            try:
                shadow = QGraphicsDropShadowEffect()
                shadow.setBlurRadius(10)
                shadow.setColor(QColor(0, 0, 0, 30))  # Semi-transparent black
                shadow.setOffset(0, 3)
                frame.setGraphicsEffect(shadow)
            except Exception as e:
                # Fall back to a simpler style if shadow effects aren't supported
                print(f"Shadow effect not applied: {e}")
                frame.setStyleSheet("""
                    QFrame {
                        border: 1px solid #dddddd;
                        border-radius: 12px;
                        background-color: white;
                        margin: 8px 4px;
                        padding: 0px;
                        border-bottom: 3px solid #dddddd;
                    }
                """)
                
    def update_sponsorship_status(self):
        """Update the sponsorship status display"""
        if not self.user:
            self.status_label.setText("No user loaded.")
            self.terminate_button.hide()
            return
        
        # Only check if the user is sponsored, don't check verification status
        # Use a more robust check for sponsored users
        is_sponsored = False
        
        # Check if the user is a SponsoredUser instance
        if isinstance(self.user, SponsoredUser):
            is_sponsored = True
        
        # Check if the user has a company_name attribute
        elif hasattr(self.user, 'company_name'):
            # Verify the attribute is not empty
            company_name = getattr(self.user, 'company_name', None)
            if company_name and isinstance(company_name, str) and company_name.strip():
                is_sponsored = True
        
        # Update the UI based on sponsorship status
        if is_sponsored:
            company_name = getattr(self.user, 'company_name', 'a company')
            self.status_label.setText(f"You are currently sponsored by {company_name}.")
            self.terminate_button.show()
        else:
            # Always show this message regardless of verification status
            self.status_label.setText(
                "Browse the sponsorship opportunities below to apply."
            )
            self.terminate_button.hide()
        
        # Force update to ensure UI reflects current state
        self.status_label.update()
        self.terminate_button.update()
        self.sponsorship_frame.update()
        
        # Force a complete repaint
        self.repaint()
        
        # Force the layout to update
        if self.layout():
            self.layout().update()
            self.layout().activate()
    
    def apply_for_sponsorship(self, company):
        """Apply for sponsorship from a company"""
        if not self.user or not self.user_controller:
            QMessageBox.warning(
                self, 
                "Error", 
                "Could not apply for sponsorship - no user loaded."
            )
            return
        
        # Check if the user is eligible and get the result
        success, message = self.company_service.apply_for_sponsorship(self.user, company)
        
        if success:
            # Apply the sponsorship
            sponsored_user, result_message = self.company_service.sponsor_user(self.user, company)
            
            # Update the user controller's reference
            self.user_controller.user = sponsored_user
            
            # Update our reference
            self.user = sponsored_user
            
            # Update the main controller's reference to the user
            from src.controllers.main_controller import MainController
            main_controller = MainController.get_instance()
            if main_controller:
                main_controller.user = sponsored_user
                if hasattr(main_controller, 'main_window'):
                    main_controller.main_window.update_user_profile()
            
            # Show success message
            QMessageBox.information(
                self, 
                "Sponsorship Approved", 
                f"Congratulations! You are now sponsored by {company.name}.\n\n"
                f"Your handle will now show the [Sponsored] tag and your bio will "
                f"indicate your sponsor."
            )
            
            # Update the UI
            self.update_sponsorship_status()
            
        else:
            # Show rejection message with the exact message from the service
            QMessageBox.warning(
                self, 
                "Sponsorship Rejected", 
                f"{message}"
            )
    
    def terminate_sponsorship(self):
        """Terminate the current sponsorship"""
        # More robust check for sponsored user
        is_sponsored = isinstance(self.user, SponsoredUser) or hasattr(self.user, 'company_name')
        
        if not is_sponsored or not self.user_controller:
            QMessageBox.warning(
                self,
                "Error",
                "You don't have an active sponsorship to terminate."
            )
            return
        
        # Get company name safely
        company_name = getattr(self.user, 'company_name', "your sponsor")
        
        # Ask for confirmation
        reply = QMessageBox.question(
            self, 
            "Confirm Termination", 
            f"Are you sure you want to terminate your sponsorship with {company_name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Remove the sponsorship
            unwrapped_user, message = self.company_service.remove_sponsorship(self.user)
            
            # Update the user controller's reference
            self.user_controller.user = unwrapped_user
            
            # Update our reference
            self.user = unwrapped_user
            
            # Update the main controller's reference to the user
            from src.controllers.main_controller import MainController
            main_controller = MainController.get_instance()
            if main_controller:
                main_controller.user = unwrapped_user
                if hasattr(main_controller, 'main_window'):
                    main_controller.main_window.update_user_profile()
            
            # Show success message
            QMessageBox.information(
                self, 
                "Sponsorship Terminated", 
                f"{message}"
            )
            
            # Update the UI
            self.update_sponsorship_status()
            self.update()
            self.repaint()
            
            # Force a complete repaint of the parent window if available
            parent = self.parent()
            while parent:
                parent.update()
                parent.repaint()
                parent = parent.parent()
    
    def update_theme_styling(self):
        """Update styling based on current theme"""
        current_theme = self.theme_manager.current_theme
        
        if current_theme == "dark":
            self.sponsorship_frame.setStyleSheet("""
                QFrame {
                    background-color: #353535;
                    border: 1px solid #444444;
                    border-radius: 8px;
                }
            """)
            
            # Update company frames for dark theme
            for i in range(self.companies_layout.count()):
                item = self.companies_layout.itemAt(i)
                if item and item.widget():
                    widget = item.widget()
                    if isinstance(widget, QFrame) and widget.property("company"):
                        self.update_company_frame_style(widget)
                        
            # Update labels in company frames
            for child in self.findChildren(QLabel):
                if child.property("company_name"):
                    child.setStyleSheet("font-weight: bold; font-size: 15px; color: #ffffff;")
                elif child.property("description"):
                    child.setStyleSheet("color: #bbbbbb; margin-top: 4px; margin-bottom: 8px; line-height: 140%;")
                    
            # Update separators
            for child in self.findChildren(QFrame):
                if child.property("separator"):
                    child.setStyleSheet("background-color: #555555; min-height: 1px; max-height: 1px; margin: 4px 0px;")
                    
        else:
            self.sponsorship_frame.setStyleSheet("""
                QFrame {
                    background-color: #f8f9fa;
                    border: 1px solid #e0e0e0;
                    border-radius: 8px;
                }
            """)
            
            # Update company frames for light theme
            for i in range(self.companies_layout.count()):
                item = self.companies_layout.itemAt(i)
                if item and item.widget():
                    widget = item.widget()
                    if isinstance(widget, QFrame) and widget.property("company"):
                        self.update_company_frame_style(widget)
                        
            # Update labels in company frames
            for child in self.findChildren(QLabel):
                if child.property("company_name"):
                    child.setStyleSheet("font-weight: bold; font-size: 15px; color: #000000;")
                elif child.property("description"):
                    child.setStyleSheet("color: #555555; margin-top: 4px; margin-bottom: 8px; line-height: 140%;")
                    
            # Update separators
            for child in self.findChildren(QFrame):
                if child.property("separator"):
                    child.setStyleSheet("background-color: #eeeeee; min-height: 1px; max-height: 1px; margin: 4px 0px;")
    
    @pyqtSlot(str)
    def on_theme_changed(self, theme):
        """Handle theme changes"""
        self.update_theme_styling() 
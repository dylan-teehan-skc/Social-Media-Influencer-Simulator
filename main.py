import sys

from PyQt6.QtWidgets import QApplication

from src.controllers.main_controller import MainController


def main():

    app = QApplication(sys.argv)

    # Create the main controller
    main_controller = MainController()

    # Show the main window
    main_controller.main_window.show()

    # Start the application event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

from lib_config.config_loader import ConfigLoader
from lib_utils.logger import setup_logger
from src.services.logger_service import LoggerService
import logging
from src.mediator.mediator import Mediator
from frontend.ui_logic import UILogic

def main():
    # Load the configuration settings for the application
    config = ConfigLoader()
    
    # Sets up the logger with full logging configuration to capture events
    logger = setup_logger(
        name=config.get('app.name'),
        config=config.get('logging')
    )
    
    # This sets the logger in the service and configures the debug level for detailed logging messages
    LoggerService.set_logger(logger)
    logger.setLevel(logging.DEBUG)

    # Initializes the mediator to handle communication between all components
    mediator = Mediator()

    # Creates the UI logic instance, which is responsible for handling user interactions
    ui_logic = UILogic(mediator)
    
    # This starts the application by running UI logic
    ui_logic.run()

if __name__ == "__main__":
    main() 
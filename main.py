from lib_config.config_loader import ConfigLoader
from lib_utils.logger import setup_logger
from src.services.logger_service import LoggerService
import logging
from src.mediator.mediator import Mediator
from frontend.ui_logic import UILogic

def main():
    # Load configuration
    config = ConfigLoader()
    
    # Setup logger with full logging config
    logger = setup_logger(
        name=config.get('app.name'),
        config=config.get('logging')
    )
    
    # Set the logger in the service and configure debug level
    LoggerService.set_logger(logger)
    logger.setLevel(logging.DEBUG)

    mediator = Mediator()
    ui_logic = UILogic(mediator)
    
    # Create and run game
    ui_logic.run()

if __name__ == "__main__":
    main() 
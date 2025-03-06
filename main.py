from lib_config.config_loader import ConfigLoader
from src.services.logger import setup_logger
from src.services.logger_service import LoggerService
import logging
from src.mediator.mediator import Mediator
from frontend.ui_logic import UILogic

def main():
    config = ConfigLoader()
    logger = setup_logger(
        name=config.get('app.name'),
        config=config.get('logging')
    )
    
    LoggerService.set_logger(logger)
    logger.setLevel(logging.DEBUG)

    logger.info("Starting the application")
    mediator = Mediator()
    ui_logic = UILogic(mediator)
    ui_logic.run()

if __name__ == "__main__":
    main() 
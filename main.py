from lib_config.config_loader import ConfigLoader
from lib_utils.logger import setup_logger
from src.services.logger_service import LoggerService
from src.classes.user import User
from src.classes.post import Post
import logging

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
    
    # Your application code here
    user = User("sloggo", "I'm a software engineer")
    post = Post("I'm a software engineer")
    print(user.posts)
if __name__ == "__main__":
    main() 
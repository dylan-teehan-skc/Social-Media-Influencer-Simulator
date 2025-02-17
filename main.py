from lib_config.config_loader import ConfigLoader
from lib_utils.logger import setup_logger

def main():
    # Load configuration
    config = ConfigLoader()
    
    # Setup logger with full logging config
    logger = setup_logger(
        name=config.get('app.name'),
        config=config.get('logging')
    )
    
    # Test different log levels
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    
    # Your application code here
    
if __name__ == "__main__":
    main() 
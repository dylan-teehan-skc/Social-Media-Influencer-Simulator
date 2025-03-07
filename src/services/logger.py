import logging
import os
import sys
from logging.handlers import RotatingFileHandler

# ANSI escape sequences for colors
COLORS = {
    'DEBUG': '\033[36m',     # Cyan
    'INFO': '\033[32m',      # Green
    'WARNING': '\033[33m',   # Yellow
    'ERROR': '\033[31m',     # Red
    'CRITICAL': '\033[41m',  # Red background
    'RESET': '\033[0m'       # Reset
}


class ColoredFormatter(logging.Formatter):
    """
    This class is responsible for formatting the log messages.
    It adds color to the log messages if the color is enabled.
    """
    
    def __init__(self, use_colors=True, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.use_colors = use_colors

    def format(self, record):
        original_levelname = record.levelname

        if self.use_colors:
            color = COLORS.get(record.levelname, COLORS['RESET'])
            record.levelname = f"{color}{record.levelname}{COLORS['RESET']}"

        result = super().format(record)

        record.levelname = original_levelname
        return result


def setup_logger(name, config):

    """Configure and return a logger instance

    Args:
        name (str): Name of the logger
        config (dict): Logging configuration from config file

    Returns:
        logging.Logger: Configured logger instance

    """
    This function is responsible for setting up the logger.
    It creates a logger instance and sets the level and format.
    It also creates a file handler and a console handler.

    """
    logger = logging.getLogger(name)
    
    level = getattr(logging, config.get('level', 'INFO').upper())
    logger.setLevel(level)
    
   
    logger.handlers = []
    

    log_format = config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Setup file logging if enabled
    file_config = config.get('file', {})
    if file_config.get('enabled', True):
        log_file = file_config.get('path', 'logs/app.log')
        max_bytes = file_config.get('max_size', 10000000) 
        backup_count = file_config.get('backup_count', 5)

        # Create logs directory if it doesn't exist
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(file_handler)

    console_config = config.get('console', {})
    if console_config.get('enabled', True):
       
        console_handler = logging.StreamHandler(sys.stdout)


        use_colors = console_config.get('colored', True)
        console_handler.setFormatter(ColoredFormatter(
            use_colors=use_colors,
            fmt=log_format
        ))
        logger.addHandler(console_handler)

    return logger

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
    """Custom formatter for colored console output"""

    def __init__(self, *args, use_colors=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_colors = use_colors

    def format(self, record):
        # Save original levelname
        original_levelname = record.levelname

        if self.use_colors:
            # Add color to the levelname
            color = COLORS.get(record.levelname, COLORS['RESET'])
            record.levelname = f"{color}{record.levelname}{COLORS['RESET']}"

        result = super().format(record)

        # Restore original levelname
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
    # Create logger
    logger = logging.getLogger(name)

    # Set base logging level
    level = getattr(logging, config.get('level', 'INFO').upper())
    logger.setLevel(level)

    # Remove existing handlers if any
    logger.handlers = []

    # Get base format
    log_format = config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Setup file logging if enabled
    file_config = config.get('file', {})
    if file_config.get('enabled', True):
        log_file = file_config.get('path', 'logs/app.log')
        max_bytes = file_config.get('max_size', 10000000)  # 10MB default
        backup_count = file_config.get('backup_count', 5)

        # Create logs directory if it doesn't exist
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        # Create file handler
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(file_handler)

    # Setup console logging if enabled
    console_config = config.get('console', {})
    if console_config.get('enabled', True):
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)

        # Use colored output if enabled
        use_colors = console_config.get('colored', True)
        console_handler.setFormatter(ColoredFormatter(
            use_colors=use_colors,
            fmt=log_format
        ))
        logger.addHandler(console_handler)

    return logger

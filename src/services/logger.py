import logging
import os
import sys
from logging.handlers import RotatingFileHandler

# ANSI color codes for terminal output
COLORS = {
    "DEBUG": "\033[36m",  # Cyan
    "INFO": "\033[32m",  # Green
    "WARNING": "\033[33m",  # Yellow
    "ERROR": "\033[31m",  # Red
    "CRITICAL": "\033[41m",  # Red background
    "RESET": "\033[0m",  # Reset
}


class ColoredFormatter(logging.Formatter):
    # Custom formatter for colored console output

    def __init__(self, *args, use_colors=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_colors = use_colors

    def format(self, record):
        # Save and restore original levelname to avoid modifying the record permanently
        original_levelname = record.levelname

        if self.use_colors:
            color = COLORS.get(record.levelname, COLORS["RESET"])
            record.levelname = f"{color}{record.levelname}{COLORS['RESET']}"

        result = super().format(record)

        record.levelname = original_levelname
        return result


def setup_logger(name, config):
    # Configure and return a logger instance

    logger = logging.getLogger(name)

    # Set logging level from config
    level = getattr(logging, config.get("level", "INFO").upper())
    logger.setLevel(level)

    # Clear existing handlers
    logger.handlers = []

    # Get log format from config
    log_format = config.get(
        "format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Setup file logging if enabled
    file_config = config.get("file", {})
    if file_config.get("enabled", True):
        log_file = file_config.get("path", "logs/app.log")
        max_bytes = file_config.get("max_size", 10000000)  # 10MB default
        backup_count = file_config.get("backup_count", 5)

        # Create logs directory
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        # Add rotating file handler
        file_handler = RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count
        )
        file_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(file_handler)

    # Setup console logging if enabled
    console_config = config.get("console", {})
    if console_config.get("enabled", True):
        console_handler = logging.StreamHandler(sys.stdout)

        # Use colored output if configured
        use_colors = console_config.get("colored", True)
        console_handler.setFormatter(
            ColoredFormatter(use_colors=use_colors, fmt=log_format)
        )
        logger.addHandler(console_handler)

    return logger

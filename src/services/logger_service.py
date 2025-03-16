import logging


class LoggerService:
    """Service for logging application events."""

    _logger = None

    @classmethod
    def set_logger(cls, logger):
        """Set the logger instance."""
        cls._logger = logger

    @classmethod
    def get_logger(cls):
        """Get the logger instance."""
        if cls._logger is None:
            # Create a default logger if none is set
            cls._logger = cls._create_default_logger()
        return cls._logger

    @staticmethod
    def _create_default_logger():
        """Create a default logger."""
        logger = logging.getLogger("Social Media Simulator")
        logger.setLevel(logging.INFO)

        # Create console handler
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(handler)

        return logger

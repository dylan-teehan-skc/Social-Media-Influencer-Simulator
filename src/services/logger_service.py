import logging


class LoggerService:
    # Service for logging application events
    _logger = None

    @classmethod
    def set_logger(cls, logger):
        # Set the logger instance
        cls._logger = logger

    @classmethod
    def get_logger(cls):
        # Get or create the logger instance
        if cls._logger is None:
            cls._logger = cls._create_default_logger()
        return cls._logger

    @staticmethod
    def _create_default_logger():
        # Create a default logger with console output
        logger = logging.getLogger("Social Media Simulator")
        logger.setLevel(logging.INFO)

        # Setup console handler with formatter
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

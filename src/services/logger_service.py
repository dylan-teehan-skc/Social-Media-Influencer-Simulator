import logging


class LoggerService:
    """
    This class is responsible for logging messages to the console.
    It uses the singleton pattern to ensure that only one instance of the logger is created.
    """
    _instance = None
    _logger = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerService, cls).__new__(cls)
        return cls._instance

    @classmethod
    def get_logger(cls):
        if cls._logger is None:
            cls._logger = logging.getLogger('Social Media Application')
        return cls._logger

    @classmethod
    def set_logger(cls, logger):
        cls._logger = logger

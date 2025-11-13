"""Logging configuration for Midnight Miner"""
import logging


def setup_logging():
    """Setup file and console logging"""
    log_format = '%(asctime)s - %(levelname)s - [%(processName)s] - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'

    logger = logging.getLogger('midnight_miner')
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    file_handler = logging.FileHandler('miner.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format, date_format))

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(logging.Formatter(log_format, date_format))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

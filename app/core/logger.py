import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime


def get_logger(
        log_level=logging.INFO,
        log_file_path="logs",
        log_file_prefix="app",
        max_file_size_mb=10,
        backup_count=5
):
    """
    Configure a logger with both file and console handlers.

    Args:
        log_level (int): Logging level (default: logging.INFO)
        log_file_path (str): Directory path for log files (default: 'logs')
        log_file_prefix (str): Prefix for log file name (default: 'app')
        max_file_size_mb (int): Maximum size of each log file in MB (default: 10)
        backup_count (int): Number of backup files to keep (default: 5)

    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    os.makedirs(log_file_path, exist_ok=True)

    # Generate log file name with timestamp
    timestamp = datetime.now().strftime('%Y%m%d')
    log_file = os.path.join(
        log_file_path,
        f"{log_file_prefix}_{timestamp}.log"
    )

    # Create logger instance
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    # Clear any existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s '
        '| %(filename)s:%(lineno)d | %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )

    # Create and configure file handler with rotation
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_file_size_mb * 1024 * 1024,  # Convert MB to bytes
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(log_level)

    # Create and configure console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(log_level)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
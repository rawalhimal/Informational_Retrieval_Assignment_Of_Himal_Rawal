# my_crawler_package/logging_config.py
import logging
import os
from datetime import datetime

def setup_logger():
    """
    Configures and sets up the logger for the application with a filename that includes the current date.

    Creates a logger that outputs messages to both a file and the console. 
    The file handler logs messages to a file in the 'logs' directory with a name that includes the current date,
    while the console handler outputs them to the console.

    Returns:
    Logger: Configured logger instance.
    """
    # Create 'logs' directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Create a filename with the current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_filename = f'logs/{current_date}.log'

    # Create logger
    logger = logging.getLogger('WebCrawlerLogger')
    logger.setLevel(logging.DEBUG)

    # Check if handlers are already added to prevent duplication
    if not logger.handlers:
        # File handler
        fh = logging.FileHandler(log_filename)
        fh.setLevel(logging.DEBUG)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger

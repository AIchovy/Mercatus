import logging
import os
import sys
from datetime import datetime

def setup_logger(name="mercatus", log_level=logging.DEBUG):
    """
    Set up and configure application logging
    
    Args:
        name: Logger name
        log_level: Log level
    
    Returns:
        Configured logger
    """
    # Create log directory
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create log filename with date
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = f"{log_dir}/{name}_{today}.log"
    
    # Configure log format
    log_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Clear existing handlers
    if logger.handlers:
        logger.handlers.clear()
    
    # Add file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
    
    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)
    
    logger.propagate = False
    
    return logger 
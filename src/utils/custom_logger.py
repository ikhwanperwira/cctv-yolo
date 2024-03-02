"""
This file contains the definition of the YOLogger class, a custom logger for the YO application.

The YOLogger class provides methods for logging info messages based on the length of a value.

Example usage:
  logger = YOLogger()
  logger.info(10, "Processing data...")
"""

import logging
from logging import Logger
from dotenv import load_dotenv

load_dotenv()

class YOLogger:
  """
  A custom logger class for YO application.
  """

  def __init__(self):
    """
    Initializes the YOLogger object.
    """
    self.logger: Logger = logging.getLogger(__class__.__name__)
    self.last_len = None

  def info(self, length, message):
    """
    Logs an info message if the length is different from the last length.

    Args:
      length (int): The length value.
      message (str): The message to log.

    Returns:
      bool: True if the message is logged, False otherwise.
    """
    if length != self.last_len:
      self.logger.info(message)
      self.last_len = length
      return True
    return False

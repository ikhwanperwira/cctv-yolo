
"""
This module provides a CameraSelector class for selecting and accessing a camera using OpenCV.

The CameraSelector class allows you to select a camera by name and provides methods to update the camera index,
check if the available camera devices have changed, and get a VideoCapture object for the selected camera.

Example:
  camera = CameraSelector(camera_name='USB CAMERA')
  video_capture = camera.get_video_capture()

Attributes:
  camera_name (str): The name of the camera to be selected.
  devices (list[str]): A list of available camera devices.
  last_dev_len (int): The length of the devices list in the previous check.
  camera_index (int): The index of the selected camera.

Methods:
  update_camera_index(): Updates the camera index based on the selected camera name.
  is_device_changed(time_hash: int = 0) -> bool: Checks if the available camera devices have changed.
  get_video_capture() -> cv.VideoCapture: Returns a VideoCapture object for the selected camera.
"""

import logging
from functools import lru_cache
from pygrabber.dshow_graph import FilterGraph
import cv2 as cv

logger: logging.Logger = logging.getLogger(__name__)

class CameraSelector:
  """
  A class for selecting and accessing a camera using OpenCV.
  """

  def __init__(self, camera_name: str = 'USB CAMERA'):
    """
    Initializes a CameraSelector object.

    Args:
      camera_name (str): The name of the camera to be selected. Defaults to 'USB CAMERA'.
    """
    self.camera_name: str = camera_name
    self.devices: list[str] = []
    self.last_dev_len : int = -1
    self.camera_index : int = -1
    self.is_device_changed()
    self.update_camera_index()

  def update_camera_index(self) -> None:
    """
    Updates the camera index based on the selected camera name.
    If the camera name is not found, the default camera index 0 is used.
    """
    try:
      logger.warning("Camera %s found, using index %s", self.camera_name, self.devices.index(self.camera_name))
      self.camera_index = self.devices.index(self.camera_name)
    except ValueError:
      logger.warning("Camera %s not found, using default camera index which is 0", self.camera_name)
      self.camera_index = 0

  @lru_cache()
  def is_device_changed(self, time_hash: int = 0) -> bool:
    """
    Checks if the available camera devices have changed.

    Args:
      time_hash (int): A hash value to force cache invalidation. Not used in this implementation.

    Returns:
      bool: True if the devices have changed, False otherwise.
    
    Raises:
      ValueError: If no cameras are found.
    """
    del time_hash
    self.devices: list[str] = FilterGraph().get_input_devices()
    dev_len: int = len(self.devices)
    if dev_len == self.last_dev_len:
      return False

    if dev_len == 0:
      logger.error("No cameras found")
      raise ValueError("No cameras found")

    logger.warning("Devices status changed, new devices: %s", self.devices)
    self.last_dev_len = dev_len
    return True

  def get_video_capture(self) -> cv.VideoCapture:
    """
    Returns a VideoCapture object for the selected camera.

    Returns:
      cv.VideoCapture: The VideoCapture object.
    """
    return cv.VideoCapture(self.camera_index)

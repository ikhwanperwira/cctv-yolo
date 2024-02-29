"""
This module contains the `frame_collector` function for collecting frames from a camera and sending them to clients.

The `frame_collector` function performs the following steps:
1. Imports necessary modules and libraries.
2. Sets up logging and creates a log file.
3. Retrieves camera settings from environment variables.
4. Initializes the camera and starts capturing frames.
5. Performs object detection on each frame.
6. Adds datetime information to the frame.
7. Saves frames with detected objects to the event folder.
8. Sends frames to connected clients.

Note: This code assumes the presence of other modules and environment variables that are not shown here.
"""

def frame_collector(clients):  # Process 1
  """
  Collects frames from a video capture device and sends them to the specified clients.

  Args:
    clients (dict): A dictionary containing client handles and senders.

  Returns:
    None

  Raises:
    KeyboardInterrupt: If the function is interrupted by a keyboard interrupt (Ctrl-C).

  """
  #pylint: disable=import-outside-toplevel
  import os
  from time import time, sleep
  import logging
  import datetime
  import io
  import cv2 as cv
  from dotenv import load_dotenv
  from utils.select_camera import CameraSelector
  from utils.custom_frame import add_datetime_with_border, perform_object_detection
  from utils.yolo import net, classes
  from .custom_logger import YOLogger
  load_dotenv()

  log_folder: str = os.getenv("LOG_FOLDER", 'logs')
  if not os.path.exists(log_folder):
    os.makedirs(log_folder)

  current_time: str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
  log_filename: str = f"{log_folder}/app_{current_time}.log"

  logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                      filename=log_filename, filemode='a')

  yologger = YOLogger()

  cam_name: str = os.getenv("CAMERA_NAME", '')
  cam_update_period: int = 3

  cam_slct = CameraSelector(camera_name=cam_name)
  cap: cv.VideoCapture = cam_slct.get_video_capture()

  is_writing = False
  try:
    while 1:
      ret, frame = cap.read()

      current_time: float = time()

      if cam_slct.is_device_changed(int(current_time) / cam_update_period):
        cap.release()
        del cap
        cap: cv.VideoCapture = cam_slct.get_video_capture()

      ret, frame = cap.read()

      if not ret:
        is_writing = False
        sleep(cam_update_period)
        continue

      # Perform object detection
      frame, counted_obj = perform_object_detection(
          frame, classes, net, yologger)
      frame = add_datetime_with_border(frame, current_time)

      if len(counted_obj) > 0:
        timestamp = str(int(current_time))
        filename = f"{timestamp}_{counted_obj}.jpg"
        event_folder = os.getenv('EVENT_FOLDER', 'events')
        cv.imwrite(os.path.join(event_folder, filename), frame)

      if not is_writing:
        is_writing = True
        buf = io.BytesIO()

      if is_writing:
        buf.write(cv.imencode('.jpg', frame)[1].tobytes())
        frame: bytes = buf.getvalue()
        d = dict(clients)
        for handle, sender in d.items():  # Make copy into local dict
          try:
            sender.send(frame)
          #pylint: disable=bare-except
          except:  # Client has gone away?
            del clients[handle]
        buf.truncate(0)
        buf.seek(0)
  except KeyboardInterrupt:  # ctrl-C
    return
  finally:
    cap.release()

"""
This module contains utility functions for manipulating frames in a video stream.

Functions:
- add_datetime_with_border(frame, current_time): Adds the current datetime with a border to the given frame.
- perform_object_detection(frame, classes, net, yologger): Performs object detection on the given frame using the specified classes and neural network.

"""

from time import localtime, strftime
from typing import Any
import cv2
import numpy as np
from dotenv import load_dotenv
from .custom_logger import YOLogger

load_dotenv()

def add_datetime_with_border(frame, current_time) -> np.ndarray:
  """
  Adds the current datetime with a border to the given frame.

  Args:
    frame (numpy.ndarray): The frame to add the datetime to.
    current_time (float): The current time in seconds since the epoch.

  Returns:
    numpy.ndarray: The frame with the datetime added.

  """
  # Get current datetime
  current_datetime: str = strftime("%Y-%b-%d %H:%M:%S UTC%z", localtime(current_time))

  # Add border
  cv2.putText(frame, current_datetime, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
  # Add text on top of the border
  cv2.putText(frame, current_datetime, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)

  return frame


def perform_object_detection(frame, classes, net, yologger: YOLogger) -> tuple:
  """
  Performs object detection on the given frame using the specified classes and neural network.

  Args:
    frame (numpy.ndarray): The frame to perform object detection on.
    classes (list): The list of class names.
    net: The neural network model for object detection.
    yologger (YOLogger): The logger for logging detection results.

  Returns:
    tuple: The frame with bounding boxes and labels drawn, and a string representing the counted objects.

  """
  # Perform object detection
  blob: Any = cv2.dnn.blobFromImage(frame, 1/255, (416, 416), swapRB=True, crop=False)
  net.setInput(blob)
  outs: Any = net.forward(net.getUnconnectedOutLayersNames())

  # Process detection results
  class_ids: list = []
  confidences: list = []
  boxes: list = []
  for out in outs:
    for detection in out:
      scores: Any = detection[5:]
      class_id: np.intp = np.argmax(scores)
      confidence: Any = scores[class_id]
      if confidence > 0.33:  # 33 adalah mAP yolov3-tiny
        center_x = int(detection[0] * frame.shape[1])
        center_y = int(detection[1] * frame.shape[0])
        width = int(detection[2] * frame.shape[1])
        height = int(detection[3] * frame.shape[0])
        left = int(center_x - width / 2)
        top = int(center_y - height / 2)
        class_ids.append(class_id)
        confidences.append(float(confidence))
        boxes.append([left, top, width, height])

  # Apply non-maximum suppression
  indices: Any = cv2.dnn.NMSBoxes(boxes, confidences, 0.33, 0.3)

  # Draw bounding boxes and labels
  is_update: bool = False
  if len(indices) > 0:
    for i in indices.flatten():
      x, y, w, h = boxes[i]
      label: Any = classes[class_ids[i]]
      confidence = confidences[i]
      cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
      cv2.putText(frame, f"{label}: {confidence:.2f}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    object_counts: dict = {}
    for i in indices.flatten():
      class_name: Any = classes[class_ids[i]]
      if class_name in object_counts:
        object_counts[class_name] += 1
      else:
        object_counts[class_name] = 1
    object_counts_str: str = ' | '.join([f"{class_name}:{count}" for class_name, count in object_counts.items()])
    is_update: bool = yologger.info(len(indices), f"Detected {len(indices)} objects; {object_counts_str}")

  counted_obj: str = ''
  if is_update:
    counted_obj: str = object_counts_str.replace(' | ', '_').replace(':', '')

  return frame, counted_obj

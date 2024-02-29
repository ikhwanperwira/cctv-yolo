"""
This file contains utility functions related to YOLO (You Only Look Once) object detection.

The YOLOv3 Tiny model is used for object detection tasks.
It is loaded using the weights, configuration, and class names files provided in the same directory as this script.
The load_yolo_model() function returns the loaded YOLOv3 Tiny model object along with a list of class names.
These class names represent the objects that the model is trained to detect.
Note: This file requires the OpenCV library (cv2) to be installed.

Author: Muhammad Ikhwan Perwira
Date: 01/Mar/2024
"""
import os
from typing import Any
import cv2 as cv

# Get the absolute path of the script
script_path: str = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute paths for the YOLOv3 Tiny model files
weights_path: str = os.path.join(script_path, "yolov3-tiny.weights")
config_path: str = os.path.join(script_path, "yolov3-tiny.cfg")
names_path: str = os.path.join(script_path, "coco.names")

# Load YOLOv3 Tiny model
net: Any = cv.dnn.readNet(weights_path, config_path)

with open(names_path, "r", encoding='utf8') as f:
  classes: list[str] = [line.strip() for line in f.readlines()]

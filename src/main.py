"""
This script starts a frame collector process and a Flask web service process to handle CCTV video streaming.

The frame collector process collects frames from multiple clients and stores them in a shared dictionary.
The Flask web service process serves the frames to clients via a web interface.

Usage:
  - Run this script to start the frame collector and Flask web service processes.
  - Access the web interface to view the CCTV video stream.

Dependencies:
  - multiprocessing: Required for running multiple processes concurrently.
  - Manager: Required for creating a shared dictionary between processes.
  - framing: Module containing the frame_collector function for collecting frames.
  - webservice: Module containing the flask_service function for serving frames.

Author: Muhammad Ikhwan Perwira
Date: 01/Mar/2024
"""
import os
import datetime
import logging
from dotenv import load_dotenv
load_dotenv()

log_folder: str = os.getenv("LOG_FOLDER", 'logs')
if not os.path.exists(log_folder):
  os.makedirs(log_folder)

current_time: str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
log_filename: str = f"{log_folder}/app_{current_time}.log"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename=log_filename, filemode='a')

if __name__ == "__main__":
  from multiprocessing import Process, Manager
  from utils.framing import frame_collector
  from utils.webservice import flask_service
  from utils.cf_config_loader import load_cf_config

  load_cf_config()

  with Manager() as manager:

    clients = manager.dict()

    p1 = Process(target=frame_collector, args=(clients,))
    p2 = Process(target=flask_service, args=(clients,))
    p1.start()
    p2.start()

    try:
      p2.join()  # block while flask_service is running
    except KeyboardInterrupt:  # ctrl-C
      p1.terminate()
      p2.terminate()
    finally:
      print('Ending up.')

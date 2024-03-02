"""
This module contains a Flask web service that streams MJPEG frames.
The `flask_service` function starts a Flask web service that streams MJPEG frames to clients.
It takes a dictionary `clients` as an argument, which is used to store client connections.
The web service is started by creating a Flask application and defining a route for MJPEG streaming.
The `frame_consumer` function is responsible for consuming frames and yielding them as MJPEG responses.
The frames are received through a multiprocessing `Pipe` and added to the `clients` dictionary.
To start the web service, the `flask_service` function calls the `app.run` method with the host set to '127.0.0.1' and threaded set to True.
Note: This code snippet contains two definitions of the `flask_service` function.
The second definition is commented out and labeled as 'Process 2'.
It imports necessary modules and sets up the frame consumer. However, it is not used in the code snippet provided.
"""

def flask_service(clients): # Process 2
  """
  Starts a Flask web service that streams MJPEG frames.

  Args:
    clients (dict): A dictionary to store client connections.

  Returns:
    None
  """
  #pylint: disable=import-outside-toplevel
  import os
  from multiprocessing import Pipe
  from flask import Flask, Response
  from dotenv import load_dotenv
  from time import time
  from glob import glob
  load_dotenv()

  app = Flask(__name__)

  def frame_consumer():
    receiver, sender = Pipe(False)
    #pylint: disable=protected-access
    clients[sender._handle] = sender
    while True:
      yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + receiver.recv() + b'\r\n'

  from flask import render_template, send_file

  # Define the directory where your static files are located
  STATIC_DIR: str = os.getenv('EVENT_FOLDER', 'events')

  @app.route('/events/<filename>')
  @app.route('/events/')
  def download_file(filename=None):
    # If filename is None, list all files
    if filename is None:
      current_time = str(int(time()))
      # Get a list of all files in the static directory
      files: list[str] = glob(f'{STATIC_DIR}/{current_time[:7]}*.jpg')
      return render_template('list_files.html', files=files)
      # Otherwise, check if the file exists and allow download
    else:
      # Get the path of the file to be downloaded
      filepath: str = os.path.join(STATIC_DIR, filename)
      # Check if the file exists
      if os.path.exists(filepath):
        # Send the file to the user for download
        return send_file(f'../../{os.getenv("EVENT_FOLDER")}/{os.path.basename(filepath)}', mimetype='image/jpeg')
      else:
        return "File not found", 404

  @app.route('/')
  def root():
    return Response(frame_consumer(),mimetype='multipart/x-mixed-replace; boundary=frame')

  app.run(host=os.getenv('HOST', '127.0.0.1'), port=int(os.getenv('PORT', '5000')), threaded=True)

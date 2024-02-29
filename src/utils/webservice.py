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
  load_dotenv()

  app = Flask(__name__)

  def frame_consumer():
    receiver, sender = Pipe(False)
    #pylint: disable=protected-access
    clients[sender._handle] = sender
    while True:
      yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + receiver.recv() + b'\r\n'

  @app.route('/')
  def mjpeg():
    return Response(frame_consumer(),mimetype='multipart/x-mixed-replace; boundary=frame')

  app.run(host=os.getenv('HOST', '127.0.0.1'), port=int(os.getenv('PORT', '5000')), threaded=True)

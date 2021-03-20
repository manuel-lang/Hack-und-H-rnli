from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)

socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True, cors_allowed_origins="*")

def send_data(eventType, data):
    socketio.emit(eventType, data,  namespace='/socket')

def main():
    socketio.run(app) # important for depoyment without container

if __name__ == '__main__':
    main()
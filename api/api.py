from flask import Flask, render_template
from flask_socketio import SocketIO

class Notification:
    recommendation_text: str
    price_change: str
    start_time: str
    end_time: str
    old_forecast: float
    new_forecast: float
    top_3_drivers: list
    confidence: float

    def init(self, recommendation_text, price_change, start_time, end_time, old_forecast, new_forecast, top_3_drives, confidence):
        self.recommendation_text = recommendation_text
        self.price_change = price_change
        self.start_time = start_time
        self.end_time = end_time
        self.old_forecast = old_forecast
        self.new_forecast = new_forecast
        self.top_3_drivers = top_3_drives
        self.confidence = confidence

app = Flask(__name__)

socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True, cors_allowed_origins="*")

def send_data(eventType: str, notification: Notification):
    socketio.emit(eventType, notification.__dict__,  namespace='/socket')


def main():
    socketio.run(app) # important for depoyment without container

if __name__ == '__main__':
    main()
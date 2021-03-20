from flask import Flask, request, render_template
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
    estimated_consumption: float
    impact_score: float

    def __init__(self, recommendation_text, price_change, start_time, end_time, old_forecast, new_forecast, top_3_drives, confidence, estimated_consumption, impact_score):
        self.recommendation_text = recommendation_text
        self.price_change = price_change
        self.start_time = start_time
        self.end_time = end_time
        self.old_forecast = old_forecast
        self.new_forecast = new_forecast
        self.top_3_drivers = top_3_drives
        self.confidence = confidence
        self.estimated_consumption = estimated_consumption
        self.impact_score = impact_score


app = Flask(__name__)

socketio = SocketIO(app, async_mode=None, logger=True,
                    engineio_logger=True, cors_allowed_origins="*")


@app.route("/notifications", methods=["POST"])
def create_notification():
    data = request.json
    noti = Notification(data["recommendation_text"], data["price_change"], data["start_time"], data["end_time"], data["old_forecast"],
                 data["new_forecast"], data["top_3_drivers"], data["confidence"], data["estimated_consumption"], data["impact_score"])
    send_data(noti)
    return data
    
@socketio.on('connect', namespace='/socket')
def test_connect():
    # need visibility of the global thread object
    print('Client connected')

@socketio.on('disconnect', namespace='/socket')
def test_disconnect():
    print('Client disconnected')

def send_data(notification: Notification):
    socketio.emit("event", notification.__dict__,  namespace='/socket')


def main():
    socketio.run(app)  # important for depoyment without container


if __name__ == '__main__':
    main()

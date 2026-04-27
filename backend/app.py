# file name: backend/app.py

from flask import Flask, Response, jsonify, send_from_directory
import detector
from detector import generate_frames
from config import JETSON_ID, LOCATION

app = Flask(
    __name__,
    static_folder="../frontend",
    static_url_path=""
)

# ---------------------------------
# Frontend Home Page
# ---------------------------------
@app.route("/")
def home():
    return send_from_directory("../frontend", "index.html")


# ---------------------------------
# Live Video Stream
# ---------------------------------
@app.route("/video")
def video():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# ---------------------------------
# Live Status API (FIXED)
# ---------------------------------
@app.route("/status")
def get_status():
    return jsonify({
        "status": detector.status,
        "drone_count": detector.drone_count,
        "jetson_id": JETSON_ID,
        "location": LOCATION
    })


# ---------------------------------
# Run Server
# ---------------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
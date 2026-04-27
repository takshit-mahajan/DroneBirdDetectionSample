# file name: backend/detector.py
# FIXED drone count logic (same visible drone won't keep increasing)

import cv2
import os
import time
from datetime import datetime
from ultralytics import YOLO

from config import MODEL_PATH, SNAPSHOT_DIR, CONFIDENCE
from logger import log_detection

os.makedirs(SNAPSHOT_DIR, exist_ok=True)

model = YOLO(MODEL_PATH)
cap = cv2.VideoCapture(0)

status = "NORMAL"
drone_count = 0

# -----------------------------------
# Anti-repeat settings
# -----------------------------------
prev_detected = False
last_seen_time = 0
cooldown_seconds = 3   # count again only if drone disappeared for 3 sec


# -----------------------------------
# Live generator
# -----------------------------------
def generate_frames():
    global status, drone_count
    global prev_detected, last_seen_time

    while True:

        success, frame = cap.read()
        if not success:
            break

        detected = False

        results = model(frame, conf=CONFIDENCE)

        for r in results:
            boxes = r.boxes

            for b in boxes:

                cls = int(b.cls[0])
                conf = float(b.conf[0])

                label = model.names[cls]

                x1, y1, x2, y2 = map(int, b.xyxy[0])

                color = (0, 0, 255)

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

                cv2.putText(
                    frame,
                    f"{label} {conf:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    color,
                    2
                )

                if "drone" in label.lower():
                    detected = True

        now = time.time()

        # -----------------------------------
        # If drone visible
        # -----------------------------------
        if detected:

            status = "ALERT"
            last_seen_time = now

            # Count only NEW event
            if not prev_detected:
                drone_count += 1

                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                path = f"{SNAPSHOT_DIR}/{ts}.jpg"

                cv2.imwrite(path, frame)
                log_detection("drone", path)

            prev_detected = True

        else:
            status = "NORMAL"

            # Reset only after cooldown
            if now - last_seen_time > cooldown_seconds:
                prev_detected = False

        # -----------------------------------
        # Stream frame
        # -----------------------------------
        ret, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" +
            frame +
            b"\r\n"
        )
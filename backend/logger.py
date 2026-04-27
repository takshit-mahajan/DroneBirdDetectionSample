import csv, os
from datetime import datetime
from config import LOG_FILE, LOCATION

os.makedirs('logs', exist_ok=True)

def log_detection(label, snapshot):
    file_exists = os.path.exists(LOG_FILE)
    with open(LOG_FILE, 'a', newline='') as f:
        w = csv.writer(f)
        if not file_exists:
            w.writerow(['time','date','label','snapshot','location'])
        now = datetime.now()
        w.writerow([now.strftime('%H:%M:%S'), now.strftime('%Y-%m-%d'), label, snapshot, LOCATION])
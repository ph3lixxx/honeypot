import os
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "activity.log")

def log_request(request):
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    with open(LOG_FILE, "a") as f:
        f.write("="*60 + "\n")
        f.write(f"Time: {datetime.utcnow().isoformat()} UTC\n")
        f.write(f"IP: {request.remote_addr}\n")
        f.write(f"Method: {request.method}\n")
        f.write(f"Path: {request.path}\n")
        f.write(f"Headers: {dict(request.headers)}\n")
        if request.method == "POST":
            f.write(f"Form Data: {request.form.to_dict()}\n")
        f.write("\n")

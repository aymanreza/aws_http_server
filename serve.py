from flask import Flask, jsonify
import subprocess
import os
import socket

app = Flask(__name__)

# Keep a handle if you want to avoid starting multiple stress processes
stress_proc = None

def get_private_ip():
    # Reliable way to get the instance's private IP (works well in EC2)
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

@app.route("/", methods=["GET"])
def handle_get():
    return jsonify({"private_ip": get_private_ip()}), 200

@app.route("/", methods=["POST"])
def handle_post():
    global stress_proc

    # If you want to allow multiple runs, remove this guard.
    if stress_proc is not None and stress_proc.poll() is None:
        return jsonify({"status": "already_running"}), 200

    script_path = os.path.join(os.path.dirname(__file__), "stress_cpu.py")

    # Start stress_cpu.py in a separate process (non-blocking)
    stress_proc = subprocess.Popen(
        ["python3", script_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return jsonify({"status": "started", "pid": stress_proc.pid}), 200

if __name__ == "__main__":
    # IMPORTANT: bind to 0.0.0.0 so ALB / other machines can reach it
    app.run(host="0.0.0.0", port=8080)
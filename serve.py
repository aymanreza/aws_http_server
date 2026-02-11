from flask import Flask
import subprocess
import os
import socket

app = Flask(__name__)

def get_private_ip():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

@app.route("/", methods=["GET"])
def handle_get():
    # Return plain string
    return get_private_ip(), 200

@app.route("/", methods=["POST"])
def handle_post():
    script_path = os.path.join(os.path.dirname(__file__), "stress_cpu.py")

    # Start a new stress process every POST
    subprocess.Popen(
        ["python3", script_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Return
    return "started", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

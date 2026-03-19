from flask import Flask, render_template, request, jsonify
import threading
import time
import main
import re
import os
import requests
from urllib.parse import urlparse

try:
    from pip._vendor import requests as pip_requests
except ImportError:
    pip_requests = None

app = Flask(__name__)

# Global state
class SpammerState:
    def __init__(self):
        self.logs = []
        self.api_logs = []
        self.stop_event = threading.Event()
        self.thread = None
        self.is_running = False
        self.target = ""

state = SpammerState()

class AbortKek(Exception):
    """Custom exception to seamlessly break out of deep script loops."""
    pass

class DummyResponse:
    def __init__(self, status_code, text=""):
        self.status_code = status_code
        self.text = text
    def json(self):
        return {}

# -- MONKEY PATCH REQUESTS API --
original_post = requests.post
original_get = requests.get
original_put = requests.put

def monitor_request(method, original_func, url, *args, **kwargs):
    if state.stop_event.is_set():
        raise AbortKek()

    domain = urlparse(url).netloc
    try:
        kwargs.setdefault('timeout', 5) # Faster timeout to skip dead APIs quickly
        res = original_func(url, *args, **kwargs)
        status = res.status_code
        is_dead = status >= 400
        state.api_logs.append({"method": method, "domain": domain, "status": status, "dead": is_dead})
        return res
    except AbortKek:
        raise
    except Exception as e:
        state.api_logs.append({"method": method, "domain": domain, "status": "FAIL: " + e.__class__.__name__, "dead": True})
        return DummyResponse(500, str(e))

requests.post = lambda url, *args, **kwargs: monitor_request("POST", original_post, url, *args, **kwargs)
requests.get = lambda url, *args, **kwargs: monitor_request("GET", original_get, url, *args, **kwargs)
requests.put = lambda url, *args, **kwargs: monitor_request("PUT", original_put, url, *args, **kwargs)

if pip_requests:
    original_pip_post = pip_requests.post
    original_pip_get = pip_requests.get
    pip_requests.post = lambda url, *args, **kwargs: monitor_request("POST", original_pip_post, url, *args, **kwargs)
    pip_requests.get = lambda url, *args, **kwargs: monitor_request("GET", original_pip_get, url, *args, **kwargs)
    main.post = pip_requests.post
    main.get = pip_requests.get

main.requests.post = requests.post
main.requests.get = requests.get
main.requests.put = requests.put

# -- PATCH TIME.SLEEP --
original_sleep = time.sleep
def stoppable_sleep(seconds):
    for _ in range(int(seconds * 10)):
        if state.stop_event.is_set():
            raise AbortKek()
        original_sleep(0.1)
main.time.sleep = stoppable_sleep

# -- PATCH MAIN FUNCTIONS --
def custom_autoketik(s):
    clean_s = re.sub(r'\033\[[0-9;]*m', '', s)
    state.logs.append(clean_s.strip())
main.autoketik = custom_autoketik

def custom_countdown(time_sec):
    for i in range(time_sec, 0, -1):
        if state.stop_event.is_set():
            raise AbortKek()
        if i % 10 == 0 or i == time_sec or i <= 5:
            state.logs.append(f"Waiting {i} seconds...")
        original_sleep(1)
main.countdown = custom_countdown

# Disable standard print inside main but keep relevant strings
def custom_print(*args, **kwargs):
    text = " ".join(str(a) for a in args)
    clean_s = re.sub(r'\033\[[0-9;]*m', '', text)
    if "Waktu" in clean_s or "Silakan Menunggu" in clean_s:
        return
    if clean_s.strip():
        state.logs.append(clean_s.strip())
main.print = custom_print

def custom_system(cmd):
    pass
main.os.system = custom_system

def custom_tanya(nomor):
    state.logs.append("Stopped by prompt logic.")
    state.stop_event.set()
main.tanya = custom_tanya

def custom_start(nomor, x):
    pass
main.start = custom_start

def spammer_worker(nomor):
    state.logs.append(f"Starting MySpamBot targeting {nomor}...")
    state.is_running = True
    state.stop_event.clear()
    state.target = nomor
    
    while not state.stop_event.is_set():
        try:
            main.jam(nomor)
        except AbortKek:
            state.logs.append("Spammer aborted by user.")
            break
        except Exception as e:
            state.logs.append(f"Error: {e}")
            break
            
    if state.target == nomor:
        state.logs.append(f"Spammer stopped for {nomor}.")
        state.is_running = False
        state.target = ""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/start", methods=["POST"])
def start_bot():
    data = request.json
    nomor = data.get("phone", "")
    if not nomor:
        return jsonify({"error": "Phone number is required."}), 400
    
    if state.is_running:
        return jsonify({"error": "Bot is already running."}), 400
        
    state.logs.clear()
    state.api_logs.clear()
    state.thread = threading.Thread(target=spammer_worker, args=(nomor,), daemon=True)
    state.thread.start()
    return jsonify({"success": True})

@app.route("/api/stop", methods=["POST"])
def stop_bot():
    if not state.is_running:
        return jsonify({"error": "Bot is not running."}), 400
        
    state.stop_event.set()
    return jsonify({"success": True})

@app.route("/api/status", methods=["GET"])
def get_status():
    last_index_logs = int(request.args.get("last_index_logs", 0))
    last_index_api = int(request.args.get("last_index_api", 0))
    
    new_logs = state.logs[last_index_logs:]
    new_api_logs = state.api_logs[last_index_api:]
    
    return jsonify({
        "is_running": state.is_running,
        "target": state.target,
        "logs": new_logs,
        "api_logs": new_api_logs,
        "last_index_logs": len(state.logs),
        "last_index_api": len(state.api_logs)
    })

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

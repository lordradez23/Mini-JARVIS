import logging
from flask import Flask, render_template, jsonify, request
import threading

app = Flask(__name__)

# Suppress Werkzeug logs to keep terminal clear of traffic
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Global state to share with the frontend
jarvis_state = {
    "status": "idle",  # idle, listening, recognizing, speaking
    "text": "Awaiting input...",
    "stats": {
        "cpu": "0%",
        "ram": "0%",
        "temp": "32°C"
    },
    "env": {
        "weather": "Fetching...",
        "time": "00:00:00"
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/state', methods=['GET', 'POST'])
def state():
    global jarvis_state
    if request.method == 'POST':
        data = request.json
        jarvis_state.update(data)
        return jsonify({"success": True})
    return jsonify(jarvis_state)

@app.route('/input', methods=['POST'])
def hud_input():
    """Receives a text command from the HUD browser UI and queues it for Jarvis."""
    import engine
    data = request.json
    text = (data or {}).get("command", "").strip()
    if text:
        engine.push_hud_input(text)
        return jsonify({"success": True, "received": text})
    return jsonify({"success": False, "error": "Empty command"}), 400

def run_server():
    app.run(port=5000, debug=False, use_reloader=False)

def start_hud():
    print("\n" + "─"*50)
    print("🌐 HUD Browser accessible at: http://127.0.0.1:5000")
    print("─"*50 + "\n")
    hud_thread = threading.Thread(target=run_server, daemon=True)
    hud_thread.start()
    return hud_thread

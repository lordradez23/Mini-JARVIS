import requests
import pyttsx3
import threading

HUD_URL = "http://127.0.0.1:5000/state"

# Shared queue for commands coming in from the HUD browser input
_hud_input_queue = []
_hud_input_lock = threading.Lock()

def push_hud_input(text):
    """Called by hud_server when a command is submitted via the browser UI."""
    with _hud_input_lock:
        _hud_input_queue.append(text)

def report_state(status, text=""):
    """Sends current Jarvis state to the HUD server."""
    try:
        requests.post(HUD_URL, json={"status": status, "text": text}, timeout=0.08)
    except:
        pass

def speak(text):
    """Converts text to speech with thread-safe initialization."""
    print(f"\nJarvis: {text}")
    report_state("speaking", text)

    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 145)
        engine.setProperty('volume', 1.0)

        voices = engine.getProperty('voices')
        for voice in voices:
            if "david" in voice.name.lower() or "zira" not in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break

        engine.say(text)
        engine.runAndWait()
        print("DEBUG: TTS Finished Speaking.")
    except Exception as e:
        print(f"TTS Error: {e}")

def listen():
    """
    Text-input mode: accepts commands from either:
      1. The terminal (type and press Enter)
      2. The HUD browser UI (submitted via the /input endpoint)
    Runs a background thread waiting for terminal input while polling
    for HUD input simultaneously.
    """
    report_state("listening", "Awaiting your command, master...")
    print("\n" + "─" * 50)
    print("  ⌨  TYPE YOUR COMMAND (or use the HUD browser):")
    print("─" * 50)

    terminal_result = [None]
    done = threading.Event()

    def terminal_thread():
        try:
            text = input("  > ").strip()
            if text:
                terminal_result[0] = text
        except (EOFError, KeyboardInterrupt):
            pass
        finally:
            done.set()

    t = threading.Thread(target=terminal_thread, daemon=True)
    t.start()

    # Poll every 100ms for either terminal input or HUD input
    while not done.is_set():
        with _hud_input_lock:
            if _hud_input_queue:
                query = _hud_input_queue.pop(0)
                done.set()
                print(f"\n  [HUD Input] Master typed: {query}")
                report_state("recognizing", f"Processing: {query}")
                return query.lower()
        done.wait(timeout=0.1)

    query = terminal_result[0]
    if not query:
        report_state("idle", "No input received.")
        return "none"

    print(f"\n  Master said: {query}")
    report_state("recognizing", f"Processing: {query}")
    return query.lower()

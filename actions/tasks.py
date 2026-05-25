import os
import re
import webbrowser
import subprocess
import psutil
import shutil
import datetime
import threading
import time
import pyperclip
import winsound


# ─────────────────────────────────────────────────────────────────
# WEB
# ─────────────────────────────────────────────────────────────────

def open_youtube(query=""):
    """Opens YouTube, optionally searching for a query."""
    if query:
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"Opening YouTube and searching for {query}."
    webbrowser.open("https://www.youtube.com")
    return "Opening YouTube, Anointed."

def search_google(query):
    """Searches Google for a query."""
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"Searching Google for: {query}."

def open_url(url):
    """Opens any URL in the default browser."""
    if not url.startswith("http"):
        url = "https://" + url
    webbrowser.open(url)
    return f"Opening {url}."


# ─────────────────────────────────────────────────────────────────
# FILES
# ─────────────────────────────────────────────────────────────────

def create_text_file(filename, content=""):
    """Creates a .txt file on the Desktop with optional content."""
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    if not filename.endswith(".txt"):
        filename += ".txt"
    filepath = os.path.join(desktop, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Created file '{filename}' on your Desktop."

def open_folder(path=""):
    """Opens a folder in Windows Explorer. Defaults to Desktop."""
    if not path:
        path = os.path.join(os.path.expanduser("~"), "Desktop")
    elif path.lower() in ("documents", "docs"):
        path = os.path.join(os.path.expanduser("~"), "Documents")
    elif path.lower() in ("downloads",):
        path = os.path.join(os.path.expanduser("~"), "Downloads")
    elif path.lower() in ("desktop",):
        path = os.path.join(os.path.expanduser("~"), "Desktop")

    if os.path.exists(path):
        subprocess.Popen(f'explorer "{path}"')
        return f"Opening folder: {path}."
    return f"I couldn't find the folder: {path}."

def read_notes():
    """Reads the JARVIS notes file and returns its contents."""
    notes_file = "jarvis_notes.txt"
    if os.path.exists(notes_file):
        with open(notes_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
        return content if content else "Your notes file is empty, Anointed."
    return "No notes file found. You haven't saved any notes yet."

def list_desktop_files():
    """Lists files on the Desktop."""
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    files = os.listdir(desktop)
    if not files:
        return "Your Desktop appears to be empty."
    names = ", ".join(files[:10])
    extra = f" and {len(files) - 10} more" if len(files) > 10 else ""
    return f"I found {len(files)} items on your Desktop: {names}{extra}."


# ─────────────────────────────────────────────────────────────────
# MESSAGING / CLIPBOARD
# ─────────────────────────────────────────────────────────────────

def draft_email(to="", subject="", body=""):
    """Opens the default mail client with a pre-filled email draft."""
    import urllib.parse
    mailto = f"mailto:{to}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
    webbrowser.open(mailto)
    return f"Opening your email client with a draft{' to ' + to if to else ''}."

def copy_to_clipboard(text):
    """Copies the given text to the system clipboard."""
    pyperclip.copy(text)
    return f"Copied to clipboard: \"{text[:60]}{'...' if len(text) > 60 else ''}\"."

def get_clipboard():
    """Reads and returns the current clipboard content."""
    content = pyperclip.paste()
    if content:
        return f"Your clipboard contains: {content[:200]}."
    return "Your clipboard is currently empty."


# ─────────────────────────────────────────────────────────────────
# MEDIA
# ─────────────────────────────────────────────────────────────────

def open_spotify():
    """Launches the Spotify desktop application."""
    os.system("start spotify")
    return "Launching Spotify, Anointed."

def media_control(action):
    """Controls media playback using keyboard shortcuts."""
    import pyautogui
    action = action.lower()
    if any(w in action for w in ["play", "pause", "resume"]):
        pyautogui.press("playpause")
        return "Toggling playback."
    elif any(w in action for w in ["next", "skip"]):
        pyautogui.press("nexttrack")
        return "Skipping to the next track."
    elif any(w in action for w in ["previous", "back", "prev"]):
        pyautogui.press("prevtrack")
        return "Going back to the previous track."
    elif "stop" in action:
        pyautogui.press("stop")
        return "Stopping playback."
    return "I didn't recognise that media command."


# ─────────────────────────────────────────────────────────────────
# PRODUCTIVITY
# ─────────────────────────────────────────────────────────────────

_pomodoro_timer = None

def start_pomodoro(minutes=25):
    """Starts a Pomodoro focus timer in a background thread."""
    from engine import speak

    try:
        minutes = int(minutes)
    except (ValueError, TypeError):
        minutes = 25

    seconds = minutes * 60

    def pomodoro_thread():
        time.sleep(seconds)
        speak(f"Anointed, your {minutes}-minute Pomodoro session is complete. Time for a short break.")
        for _ in range(4):
            winsound.Beep(880, 400)
            time.sleep(0.3)

    t = threading.Thread(target=pomodoro_thread, daemon=True)
    t.start()
    return f"Pomodoro timer started. I'll alert you in {minutes} minutes, Anointed. Stay focused."

def add_todo(item):
    """Appends an item to the to-do list file."""
    todo_file = "jarvis_todo.txt"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(todo_file, "a", encoding="utf-8") as f:
        f.write(f"[ ] {item}  ({timestamp})\n")
    return f"Added to your to-do list: \"{item}\"."

def read_todos():
    """Reads and speaks the to-do list."""
    todo_file = "jarvis_todo.txt"
    if os.path.exists(todo_file):
        with open(todo_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if content:
            items = content.split("\n")
            return f"You have {len(items)} items on your to-do list. " + ". ".join(items[:5]) + ("..." if len(items) > 5 else "")
        return "Your to-do list is empty."
    return "You have no to-do list yet. Ask me to add something."

def clear_todos():
    """Clears the entire to-do list."""
    todo_file = "jarvis_todo.txt"
    if os.path.exists(todo_file):
        open(todo_file, "w").close()
        return "Your to-do list has been cleared."
    return "There's nothing on your to-do list to clear."


# ─────────────────────────────────────────────────────────────────
# SYSTEM INFO
# ─────────────────────────────────────────────────────────────────

def check_disk_space():
    """Reports disk usage for each drive."""
    results = []
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            free_gb  = usage.free  / (1024 ** 3)
            total_gb = usage.total / (1024 ** 3)
            pct_used = usage.percent
            results.append(
                f"Drive {part.device}: {free_gb:.1f} GB free of {total_gb:.1f} GB ({pct_used}% used)"
            )
        except PermissionError:
            continue
    return ". ".join(results) if results else "Could not retrieve disk information."

def list_running_processes(top_n=8):
    """Lists the top N processes by CPU usage."""
    procs = []
    for p in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
        try:
            procs.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # Sort by cpu_percent
    procs = sorted(procs, key=lambda x: x.get('cpu_percent', 0), reverse=True)[:top_n]
    names = [p['name'] for p in procs if p.get('name')]
    return f"Top running processes by CPU: {', '.join(names)}."

def get_network_status():
    """Returns basic network stats."""
    net = psutil.net_io_counters()
    sent_mb = net.bytes_sent / (1024 ** 2)
    recv_mb = net.bytes_recv / (1024 ** 2)
    return f"Network: {sent_mb:.1f} MB sent, {recv_mb:.1f} MB received this session."

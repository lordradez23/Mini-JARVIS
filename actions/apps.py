import os
import webbrowser

def open_website(url):
    """Opens a website in the default browser."""
    webbrowser.open(url)

def open_app(app_name):
    """Opens a system application."""
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "browser": "start msedge",
        "spotify": "start spotify"
    }
    app_cmd = apps.get(app_name.lower())
    if app_cmd:
        os.system(app_cmd)
        return f"Opening {app_name} for you, Anointed."
    return f"I don't have a shortcut for {app_name} yet."

def close_app(app_name):
    """Closes a system application."""
    os.system(f"taskkill /F /IM {app_name}.exe")
    return f"Attempted to close {app_name}."

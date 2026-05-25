import os
import datetime
import pyautogui
import psutil
import threading
import time
import re
import winsound

def take_screenshot():
    """Takes a screenshot and saves it."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    pyautogui.screenshot(filename)
    return f"Screenshot saved as {filename}."

def control_volume(action):
    """Basic volume control (UP, DOWN, MUTE)."""
    if "up" in action.lower():
        pyautogui.press("volumeup")
    elif "down" in action.lower():
        pyautogui.press("volumedown")
    elif "mute" in action.lower():
        pyautogui.press("volumemute")
    return "Volume adjusted."

def get_hardware_stats():
    """Returns a summary of CPU, RAM, and Battery status."""
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    battery = psutil.sensors_battery()
    
    stats = f"CPU usage is at {cpu_usage} percent. RAM is at {ram_usage} percent."
    if battery:
        stats += f" Battery is at {battery.percent} percent."
    return stats

def system_state(action):
    """Handles deep system commands like shutdown, restart, sleep."""
    if "shutdown" in action:
        os.system("shutdown /s /t 1")
    elif "restart" in action:
        os.system("shutdown /r /t 1")
    elif "sleep" in action:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    return f"Initiating system {action}."

def set_alarm(time_string):
    """Sets a simple local alarm in a background thread."""
    from engine import speak 
    
    match = re.search(r'(\d+)\s*minute', time_string.lower())
    if match:
        minutes = int(match.group(1))
        seconds = minutes * 60
        
        def alarm_thread():
            time.sleep(seconds)
            speak(f"Anointed, your alarm for {minutes} minutes is ringing.")
            for _ in range(3):
                winsound.Beep(1000, 500)
                time.sleep(0.5)

        threading.Thread(target=alarm_thread, daemon=True).start()
        return f"I have set an alarm for {minutes} minutes."
    
    match = re.search(r'(\d+)\s*second', time_string.lower())
    if match:
        seconds = int(match.group(1))
        
        def alarm_thread():
            time.sleep(seconds)
            speak(f"Anointed, your alarm for {seconds} seconds is ringing.")
            for _ in range(3):
                winsound.Beep(1000, 500)
                time.sleep(0.5)

        threading.Thread(target=alarm_thread, daemon=True).start()
        return f"I have set an alarm for {seconds} seconds."

    return "I couldn't understand the time duration for the alarm."

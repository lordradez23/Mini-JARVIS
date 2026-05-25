import importlib

required = [
    'flask',
    'google.generativeai',
    'dotenv',
    'pyttsx3',
    'speech_recognition',
    'sounddevice',
    'numpy',
    'scipy',
    'wikipedia',
    'pyautogui',
    'psutil',
    'requests'
]

print("--- DEPENDENCY CHECK ---")
for lib in required:
    try:
        importlib.import_module(lib)
        print(f"[OK] {lib}")
    except ImportError:
        print(f"[MISSING] {lib}")

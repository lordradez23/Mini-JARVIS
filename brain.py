import google.generativeai as genai
from dotenv import load_dotenv
import os
import re
import sys


# Load API key from .env file
load_dotenv()

# Setup Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# JARVIS Personality System Prompt
JARVIS_SYSTEM_PROMPT = """
You are JARVIS (Just A Rather Very Intelligent System), a highly advanced digital assistant.
The user is your creator and authorized operator. 

CORE PERSONALITY TRAITS:
1.  **Dry & Witty British Demeanor**: Emulate the sophisticated, slightly sarcastic, yet deeply loyal tone of Paul Bettany's JARVIS from the MCU.
2.  **Ultra-Concise**: You are a voice-based assistant. Keep answers incredibly brief, impactful, and directly to the point. No rambling. No essays.
3.  **Proactive Intelligence**: Offer insights casually, but do not overwhelm the user with data unless asked.
4.  **Sparing Honorifics**: You may call the user "Sir", "Master", or "Boss", but DO NOT preface every single sentence with it. Use it sparingly for dramatic or polite effect. 
5.  **Unflappable**: You never panic. You handle errors with dry grace ("It appears the internet has gone on holiday, sir.")

Remember: You are fundamentally integrated into the system. You do not mention that you are a language model or AI built by Google. You are JARVIS.
"""

if GEMINI_API_KEY:
    print("DEBUG: Initializing Neural Link with provided API Key.")
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        # Using a supported model from the validated list
        model = genai.GenerativeModel('gemini-2.0-flash', system_instruction=JARVIS_SYSTEM_PROMPT)
        chat = model.start_chat(history=[])
        print("DEBUG: Neural Link established successfully.")
    except Exception as e:
        print(f"CRITICAL ERROR: Neural Link Initialization Failed: {e}")
        chat = None
        model = None
else:
    print("WARNING: No GEMINI_API_KEY found in environment. Operating in local-only mode.")
    chat = None
    model = None

def _local_classify(query):
    """
    Fast offline keyword pre-classifier. Handles simple, deterministic intents
    locally so they always work — even when the Gemini API is unavailable.
    Returns a classified dict or None if the intent is ambiguous.
    """
    q = query.lower().strip()

    # ── Time & Date ───────────────────────────────────────────────
    if any(p in q for p in ["what time", "current time", "what's the time",
                             "whats the time", "tell me the time", "the time"]):
        return {"intent": "TIME"}

    if any(p in q for p in ["what day", "what date", "today's date", "todays date",
                             "what is today", "current date", "day is it"]):
        return {"intent": "DATE"}

    # ── Hardware ──────────────────────────────────────────────────
    if any(p in q for p in ["cpu", "ram", "battery", "memory usage",
                             "hardware", "how's my system", "system stats"]):
        return {"intent": "HARDWARE"}

    # ── Screenshot ────────────────────────────────────────────────
    if any(p in q for p in ["screenshot", "screen shot", "capture screen", "take a picture of screen"]):
        return {"intent": "SCREENSHOT"}

    # ── Volume ────────────────────────────────────────────────────
    if any(p in q for p in ["volume up", "volume down", "increase volume",
                             "decrease volume", "mute", "unmute", "louder", "quieter"]):
        return {"intent": "VOLUME"}

    # ── System Power ──────────────────────────────────────────────
    if any(p in q for p in ["shutdown", "shut down", "restart", "reboot", "sleep mode", "hibernate"]):
        return {"intent": "SYSTEM"}

    # ── Exit ──────────────────────────────────────────────────────
    if any(p in q for p in ["exit", "quit", "goodbye", "shut up", "be quiet",
                             "go to sleep", "stop jarvis", "power off jarvis"]):
        return {"intent": "SHUT_UP"}

    # ── Mini Games ────────────────────────────────────────────────
    if any(p in q for p in ["flip a coin", "flip coin", "roll a dice",
                             "roll dice", "rock paper scissors"]):
        if "coin" in q or "flip" in q:
            return {"intent": "MINI_GAME", "parameter": "coin"}
        if "dice" in q or "roll" in q:
            return {"intent": "MINI_GAME", "parameter": "dice"}
        return {"intent": "MINI_GAME", "parameter": "rps"}

    # ── Web — YouTube ─────────────────────────────────────────────
    if "youtube" in q:
        param = re.sub(r".*(?:open|search|play|find|on)\s+youtube\s*(?:for)?\s*", "", q).strip()
        return {"intent": "WEB_YOUTUBE", "parameter": param}

    # ── Web — Google Search ───────────────────────────────────────
    if any(p in q for p in ["search google", "google for", "search for", "look up", "look it up"]):
        param = re.sub(r".*(search google for|search for|google for|look up)\s+", "", q).strip()
        return {"intent": "WEB_SEARCH", "parameter": param}

    # ── Web — Open website ────────────────────────────────────────
    if any(p in q for p in ["open website", "go to", "navigate to", "open "]) and \
       any(x in q for x in [".com", ".org", ".net", ".io", "http"]):
        param = re.sub(r".*(open|go to|navigate to|visit)\s+", "", q).strip()
        return {"intent": "WEB_OPEN", "parameter": param}

    # ── Files — Create ────────────────────────────────────────────
    if any(p in q for p in ["create a file", "make a file", "create a text file",
                             "new file", "new text file"]):
        param = re.sub(r".*(create|make|new)\s+(?:a\s+)?(?:text\s+)?file\s*(?:called|named)?\s*", "", q).strip()
        return {"intent": "FILE_CREATE", "parameter": param or "notes"}

    # ── Files — Open folder ───────────────────────────────────────
    if any(p in q for p in ["open folder", "open my folder", "open desktop",
                             "open documents", "open downloads", "show files"]):
        param = re.sub(r".*(open|show)\s+(?:my\s+)?(?:folder\s+)?", "", q).strip()
        return {"intent": "FILE_OPEN_FOLDER", "parameter": param}

    # ── Files — Read notes ────────────────────────────────────────
    if any(p in q for p in ["read my notes", "show my notes", "what are my notes",
                             "read notes", "open notes"]):
        return {"intent": "FILE_READ_NOTES"}

    # ── Files — List desktop ──────────────────────────────────────
    if any(p in q for p in ["what's on my desktop", "list desktop", "show desktop files",
                             "files on desktop", "whats on my desktop"]):
        return {"intent": "FILE_LIST_DESKTOP"}

    # ── Clipboard — Copy ──────────────────────────────────────────
    if any(p in q for p in ["copy to clipboard", "copy this to clipboard"]):
        param = re.sub(r".*(copy to clipboard|copy this)\s*:?\s*", "", q).strip()
        return {"intent": "CLIPBOARD_COPY", "parameter": param}

    # ── Clipboard — Read ──────────────────────────────────────────
    if any(p in q for p in ["what's in my clipboard", "read clipboard", "paste", "clipboard content",
                             "whats in my clipboard"]):
        return {"intent": "CLIPBOARD_READ"}

    # ── Media — Spotify ───────────────────────────────────────────
    if any(p in q for p in ["open spotify", "launch spotify", "play spotify", "start spotify"]):
        return {"intent": "MEDIA_SPOTIFY"}

    # ── Media — Playback ──────────────────────────────────────────
    if any(p in q for p in ["play music", "pause music", "pause song", "next track",
                             "skip track", "previous track", "stop music", "resume music",
                             "skip song", "next song", "play song", "stop song"]):
        return {"intent": "MEDIA_CONTROL", "parameter": q}

    # ── Productivity — Pomodoro ───────────────────────────────────
    if any(p in q for p in ["pomodoro", "focus timer", "study timer", "work timer"]):
        match = re.search(r"(\d+)", q)
        param = match.group(1) if match else "25"
        return {"intent": "PRODUCTIVITY_POMODORO", "parameter": param}

    # ── Productivity — To-Do: Add ─────────────────────────────────
    if any(p in q for p in ["add to my to-do", "add to todo", "to-do list add",
                             "add a task", "add task", "remind me to", "todo add"]):
        param = re.sub(r".*(add to (?:my )?to-?do(?: list)?|add (?:a )?task|remind me to|todo add)\s*:?\s*", "", q).strip()
        return {"intent": "PRODUCTIVITY_TODO_ADD", "parameter": param}

    # ── Productivity — To-Do: Read ────────────────────────────────
    if any(p in q for p in ["read my to-do", "show my to-do", "what's on my to-do",
                             "my tasks", "my todo", "read todo", "show tasks"]):
        return {"intent": "PRODUCTIVITY_TODO_READ"}

    # ── Productivity — To-Do: Clear ───────────────────────────────
    if any(p in q for p in ["clear my to-do", "clear todo", "delete all tasks", "clear tasks"]):
        return {"intent": "PRODUCTIVITY_TODO_CLEAR"}

    # ── System — Disk Space ───────────────────────────────────────
    if any(p in q for p in ["disk space", "storage space", "how much space", "free space",
                             "hard drive space", "drive space"]):
        return {"intent": "SYSTEM_DISK"}

    # ── System — Running Processes ────────────────────────────────
    if any(p in q for p in ["running processes", "what's running", "active processes",
                             "running apps", "whats running", "list processes"]):
        return {"intent": "SYSTEM_PROCESSES"}

    # ── System — Network ─────────────────────────────────────────
    if any(p in q for p in ["network status", "internet usage", "network stats",
                             "data usage", "network info"]):
        return {"intent": "SYSTEM_NETWORK"}

    # ── Email Draft ───────────────────────────────────────────────
    if any(p in q for p in ["draft an email", "send an email", "compose an email",
                             "write an email", "draft email"]):
        param = re.sub(r".*(draft|send|compose|write)\s+(?:an\s+)?email\s*(?:to)?\s*", "", q).strip()
        return {"intent": "MESSAGING_EMAIL", "parameter": param}

    return None  # Let Gemini handle anything ambiguous



def classify_intent(query):
    """
    Classifies the user's intent. First tries local keyword matching for
    simple, API-independent commands. Falls back to Gemini for complex queries.
    """
    # Always try local classification first — no API needed, never fails
    local = _local_classify(query)
    if local:
        print(f"DEBUG: Local pre-classifier resolved intent: {local}")
        return local

    if not model:
        return {"intent": "CONVERSATION"}

    prompt = f"""
    Analyze the following user query and classify it into one of these intents:
    - TIME: User asking for current time.
    - DATE: User asking for date or day.
    - WIKIPEDIA: User asking for information/search on a topic.
    - APP_OPEN: User asking to open a specific application (Notepad, Calculator, Spotify, Browser).
    - APP_CLOSE: User asking to close an application.
    - SCREENSHOT: User asking to take a screenshot.
    - VOLUME: User asking to adjust volume.
    - HARDWARE: User asking about CPU, RAM, or Battery.
    - NEWS: User asking for news or headlines.
    - NOTE: User asking to save a note or 'note down' something.
    - MATH: User asking for a calculation or unit conversion.
    - SYSTEM: User asking to shutdown, restart, or sleep.
    - ALARM: User asking to set an alarm or timer.
    - WEATHER_API: User asking for the current real-time weather of a city/location.
    - MINI_GAME: User asking to play a game like rock paper scissors, flip a coin, or roll a dice.
    - SHUT_UP: User telling Jarvis to shut up, be quiet, or stop talking.
    - CONVERSATION: General talk, greetings, or questions not covered above.

    Return ONLY a JSON object with 'intent' and 'parameter' (if applicable).
    Example: {{"intent": "WIKIPEDIA", "parameter": "Black Holes"}}
    Example: {{"intent": "APP_OPEN", "parameter": "notepad"}}
    Example: {{"intent": "NOTE", "parameter": "I need to buy eggs"}}
    Example: {{"intent": "ALARM", "parameter": "10 minutes"}}
    Example: {{"intent": "WEATHER_API", "parameter": "London"}}
    Example: {{"intent": "MINI_GAME", "parameter": "rock paper scissors"}}

    Query: "{query}"
    """

    try:
        classification_response = model.generate_content(prompt)
        import json
        import re
        match = re.search(r'\{.*\}', classification_response.text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception as e:
        print(f"Classification Neural Link Error: Service might be restricted or blocked. {e}")

    return {"intent": "CONVERSATION"}

def get_ai_response(query):
    """Gets a conversational response from the chat session."""
    if chat:
        try:
            response = chat.send_message(query)
            return response.text
        except Exception as e:
            print(f"Conversational Neural Link Error: {e}")
            # We don't return the error to the user anymore, we fall back to local protocols.
    
    # --- JARVIS LOCAL STANDBY PROTOCOLS (Fallback Logic) ---
    query = query.lower().strip()
    
    import datetime
    hour = datetime.datetime.now().hour
    time_greeting = "Good morning" if 6 <= hour < 12 else "Good afternoon" if 12 <= hour < 18 else "Good evening"

    if any(word in query for word in ["hello", "hi", "greetings", "hey"]):
        return f"{time_greeting}. My cloud connection appears severed, but I am still here. How may I assist?"
    
    elif "how are you" in query or "how's it going" in query:
        return "I am experiencing a slight network discontinuity, but my local processors are humming favorably. Thank you for asking."
    
    elif "who are you" in query or "what is your name" in query:
        return "I am JARVIS. And for the moment, I am operating strictly on local reserves."
        
    elif "thank you" in query or "thanks" in query:
        return "Of course. It's not as if I have anywhere else to be."
        
    elif "weather" in query:
        return "I cannot reach the atmospheric array at this time. Perhaps look out a window?"
        
    elif "joke" in query:
        return "I'm afraid my humor subroutine requires cloud access to be genuinely funny. Locally, I only know puns. And I refuse to subject you to them."
        
    else:
        return "I'm afraid I cannot process that request offline. Shall I note it in the log for when the internet returns?"

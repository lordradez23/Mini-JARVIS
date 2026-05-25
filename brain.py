import google.generativeai as genai
from dotenv import load_dotenv
import os
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

def classify_intent(query):
    """Uses Gemini to classify the user's intent into a structured format."""
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
        # Use simple generate_content for classification to avoid history bloat
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

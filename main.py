import engine
import actions
import brain
import hud_server
import os
import sys
import datetime
import random
import requests
import threading
import time
import psutil
from engine import report_state


def main():
    """Main execution loop for Jarvis with intelligent intent routing."""
    # Launch the Visual HUD server in the background
    hud_server.start_hud()

    # Launch telemetry thread to sync real stats with HUD
    def telemetry_loop():
        while True:
            try:
                cpu = f"{psutil.cpu_percent()}%"
                ram = f"{psutil.virtual_memory().percent}%"
                # Mock temperature if sensor doesn't exist on windows
                temp = "38°C"
                
                now = datetime.datetime.now().strftime("%H:%M:%S")
                
                # Fetch recent weather from HUD state or mock if too frequent
                # For now, just send hardware
                requests.post("http://127.0.0.1:5000/state", json={
                    "stats": {"cpu": cpu, "ram": ram, "temp": temp},
                    "env": {"time": now, "weather": "Operational"}
                }, timeout=1)
            except:
                pass
            time.sleep(2)

    threading.Thread(target=telemetry_loop, daemon=True).start()
    
    # 1. Situational Greeting
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        greeting = "Good morning Anointed."
    elif 12 <= hour < 18:
        greeting = "Good afternoon Anointed."
    else:
        greeting = "Good evening Anointed."
    
    engine.speak(f"Initializing Jarvis... {greeting}")
    engine.speak("All systems are online. My neural links are synchronized and I am ready to assist.")

    while True:
        query = engine.listen()

        if query.lower() == "none" or not query:
            continue

        # --- INTELLIGENT ROUTING (Deep Understanding) ---
        try:
            # We use Gemini to classify the intent of your natural speech
            classification = brain.classify_intent(query)
            intent = classification.get("intent", "CONVERSATION")
            parameter = classification.get("parameter", "")

            print(f"DEBUG: Classified Intent: {intent} | Parameter: {parameter}")

            # 1. Time & Date
            if intent == "TIME":
                time_str = actions.get_time()
                engine.speak(f"The current time is {time_str}")

            elif intent == "DATE":
                date_str = actions.get_date()
                engine.speak(f"Today is {date_str}")

            # 2. Web & Knowledge
            elif intent == "WIKIPEDIA":
                search_query = parameter if parameter else query
                engine.speak(f"Searching my internal database for {search_query}...")
                result = actions.search_wikipedia(search_query)
                engine.speak(result)

            # 3. Application Control
            elif intent == "APP_OPEN":
                app_name = parameter if parameter else query
                msg = actions.open_app(app_name)
                engine.speak(msg)

            elif intent == "APP_CLOSE":
                app_name = parameter if parameter else query
                msg = actions.close_app(app_name)
                engine.speak(msg)

            # 4. System Controls
            elif intent == "SCREENSHOT":
                msg = actions.take_screenshot()
                engine.speak(msg)

            elif intent == "VOLUME":
                if "up" in query or "increase" in query: 
                    actions.control_volume("up")
                    engine.speak("Increasing volume.")
                elif "down" in query or "decrease" in query: 
                    actions.control_volume("down")
                    engine.speak("Decreasing volume.")
                elif "mute" in query: 
                    actions.control_volume("mute")
                    engine.speak("Toggling mute.")

            elif intent == "HARDWARE":
                stats = actions.get_hardware_stats()
                engine.speak(stats)

            elif intent == "NEWS":
                engine.speak("Fetching the latest headlines for you, Anointed.")
                headlines = actions.get_news()
                engine.speak(headlines)

            elif intent == "SYSTEM":
                if "shutdown" in query:
                    engine.speak("Initiating system shutdown. Goodbye Anointed.")
                    actions.system_state("shutdown")
                elif "restart" in query:
                    engine.speak("Restarting all systems.")
                    actions.system_state("restart")
                elif "sleep" in query:
                    engine.speak("Entering low power mode.")
                    actions.system_state("sleep")

            # 5. Productivity & Math
            elif intent == "NOTE":
                note_content = parameter if parameter else query
                msg = actions.save_note(note_content)
                engine.speak(msg)

            elif intent == "MATH":
                if "convert" in query:
                    # Let the updated convert_units handle the whole string
                    engine.speak(actions.convert_units(query))
                else:
                    expr = (parameter or query)
                    engine.speak(actions.calculate(expr))

            # 6. Practical Tools & Fun
            elif intent == "ALARM":
                duration = parameter if parameter else query
                msg = actions.set_alarm(duration)
                engine.speak(msg)
                
            elif intent == "WEATHER_API":
                location = parameter if parameter else "your current location"
                msg = actions.get_weather(location)
                engine.speak(msg)
                
            elif intent == "MINI_GAME":
                game_type = parameter if parameter else "rps" # Default to rock paper scissors
                if "coin" in query or "flip" in query:
                    game_type = "coin"
                elif "dice" in query or "roll" in query:
                    game_type = "dice"
                
                # Simple interaction loop for RPS
                if game_type == "rps":
                    engine.speak("Rock, paper, or scissors?")
                    user_choice = engine.listen().lower()
                    if any(x in user_choice for x in ["rock", "paper", "scissors"]):
                        choice = "rock" if "rock" in user_choice else "paper" if "paper" in user_choice else "scissors"
                        msg = actions.play_mini_game("rps", choice)
                    else:
                        msg = "I couldn't understand your choice, Anointed."
                else:
                    msg = actions.play_mini_game(game_type)
                    
                engine.speak(msg)

            # 7. Exit/Stop
            elif intent == "SHUT_UP" or any(word in query for word in ["exit", "quit", "stop", "goodbye", "go to sleep", "shut up", "be quiet"]):
                variations = [
                    "Goodbye Anointed. I'll be here if you need me.",
                    "Shutting down. Have a pleasant evening, sir.",
                    "All systems offline. Farewell.",
                    "As you wish, sir. Silencing all protocols.",
                    "Understood, Anointed. I shall remain silent."
                ]
                engine.speak(random.choice(variations))
                break

            # ── Web ──────────────────────────────────────────────────
            elif intent == "WEB_YOUTUBE":
                engine.speak(actions.open_youtube(parameter))

            elif intent == "WEB_SEARCH":
                engine.speak(actions.search_google(parameter or query))

            elif intent == "WEB_OPEN":
                engine.speak(actions.open_url(parameter or query))

            # ── Files ─────────────────────────────────────────────────
            elif intent == "FILE_CREATE":
                name = parameter.strip() or "jarvis_new_file"
                engine.speak(actions.create_text_file(name))

            elif intent == "FILE_OPEN_FOLDER":
                engine.speak(actions.open_folder(parameter))

            elif intent == "FILE_READ_NOTES":
                content = actions.read_notes()
                engine.speak(content)

            elif intent == "FILE_LIST_DESKTOP":
                engine.speak(actions.list_desktop_files())

            # ── Clipboard ─────────────────────────────────────────────
            elif intent == "CLIPBOARD_COPY":
                if parameter:
                    engine.speak(actions.copy_to_clipboard(parameter))
                else:
                    engine.speak("What would you like me to copy, Anointed?")

            elif intent == "CLIPBOARD_READ":
                engine.speak(actions.get_clipboard())

            # ── Media ─────────────────────────────────────────────────
            elif intent == "MEDIA_SPOTIFY":
                engine.speak(actions.open_spotify())

            elif intent == "MEDIA_CONTROL":
                engine.speak(actions.media_control(parameter or query))

            # ── Productivity ──────────────────────────────────────────
            elif intent == "PRODUCTIVITY_POMODORO":
                mins = parameter if parameter else "25"
                engine.speak(actions.start_pomodoro(mins))

            elif intent == "PRODUCTIVITY_TODO_ADD":
                if parameter:
                    engine.speak(actions.add_todo(parameter))
                else:
                    engine.speak("What would you like to add to your to-do list, Anointed?")

            elif intent == "PRODUCTIVITY_TODO_READ":
                engine.speak(actions.read_todos())

            elif intent == "PRODUCTIVITY_TODO_CLEAR":
                engine.speak(actions.clear_todos())

            # ── System Info ───────────────────────────────────────────
            elif intent == "SYSTEM_DISK":
                engine.speak(actions.check_disk_space())

            elif intent == "SYSTEM_PROCESSES":
                engine.speak(actions.list_running_processes())

            elif intent == "SYSTEM_NETWORK":
                engine.speak(actions.get_network_status())

            # ── Messaging ─────────────────────────────────────────────
            elif intent == "MESSAGING_EMAIL":
                engine.speak(actions.draft_email(to=parameter))

            # 8. Conversational Response (The Soul of JARVIS)
            else:
                response = brain.get_ai_response(query)
                engine.speak(response)

        except Exception as e:
            print(f"CRITICAL ERROR IN MAIN LOOP: {e}")
            engine.speak("I seem to have encountered a critical error processing that request, sir. Shall we try again?")


if __name__ == "__main__":
    main()

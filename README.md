# 🤖 Mini JARVIS
### *Just A Rather Very Intelligent System*

> *"All systems are online. My neural links are synchronized and I am ready to assist."*

A Python-powered AI assistant inspired by the MCU's JARVIS, featuring a real-time holographic HUD, Google Gemini intelligence, intelligent intent routing, and Text-to-Speech output — all controllable via typed commands in the terminal or directly through the browser.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Jarvis](#running-jarvis)
- [How to Use](#how-to-use)
- [Command Reference](#command-reference)
- [Modules](#modules)
- [HUD Dashboard](#hud-dashboard)
- [Offline Mode](#offline-mode)
- [Troubleshooting](#troubleshooting)
- [Dependencies](#dependencies)

---

## Overview

Mini JARVIS is a desktop AI assistant that combines:

- 🧠 **Google Gemini 2.0 Flash** for natural language understanding and conversational AI
- 🔊 **pyttsx3 Text-to-Speech** for spoken responses delivered in a calm, masculine voice
- 🎯 **Intelligent Intent Routing** — Gemini classifies each command into one of 16 action categories
- 🖥️ **Live HUD Dashboard** — A sci-fi browser interface showing system stats, live status, and a command input bar
- ⌨️ **Text Input Mode** — Commands accepted via terminal prompt or the HUD browser UI

---

## Features

| Category | Capability |
|---|---|
| 🕐 **Time & Date** | Current time, today's date |
| 🌐 **Knowledge** | Wikipedia search and summaries |
| 📱 **App Control** | Open/close Notepad, Calculator, Spotify, Browser, etc. |
| 📸 **System Tools** | Screenshots, volume control, hardware stats |
| ⚙️ **System Power** | Shutdown, restart, sleep |
| 📰 **News** | Latest headlines |
| 📝 **Notes** | Save notes to a local file |
| 🧮 **Math & Conversions** | Arithmetic calculations and unit conversions |
| ⏰ **Alarms** | Timed alarms with audio beep |
| 🌤️ **Weather** | Real-time weather by city/location |
| 🎮 **Mini Games** | Rock-Paper-Scissors, coin flip, dice roll |
| 💬 **Conversation** | Full conversational AI with JARVIS personality |
| 🖥️ **Live HUD** | Real-time CPU, RAM, temp, clock, status display |

---

## Project Structure

```
Mini_jarvis/
│
├── main.py               # Entry point — main event loop & intent routing
├── brain.py              # Gemini AI integration, intent classifier, personality
├── engine.py             # Text-to-Speech (speak) & text input (listen)
├── hud_server.py         # Flask server powering the HUD dashboard
│
├── actions/              # Modular action handlers
│   ├── __init__.py       # Re-exports all actions
│   ├── system.py         # Screenshots, volume, hardware, alarms, system power
│   ├── apps.py           # Open/close applications
│   ├── utility.py        # Time, date, weather, Wikipedia, news, notes
│   ├── logic.py          # Math calculations & unit conversions
│   └── games.py          # Rock-Paper-Scissors, coin flip, dice roll
│
├── templates/
│   └── index.html        # HUD browser interface
│
├── static/
│   ├── style.css         # Sci-fi HUD styling
│   ├── hud.js            # HUD state polling & animation logic
│   └── particles.js      # Background particle animation
│
├── .env                  # API keys (never commit this)
├── requirements.txt      # Python dependencies
└── README.md             # You are here
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                        main.py                          │
│  ┌──────────┐   ┌───────────────┐   ┌───────────────┐  │
│  │ listen() │──▶│ classify_intent│──▶│ Action Router │  │
│  │ engine   │   │   brain.py    │   │  (16 intents) │  │
│  └──────────┘   └───────────────┘   └───────┬───────┘  │
│       ▲                                      │          │
│       │                              ┌───────▼───────┐  │
│  ┌────┴──────┐                      │  actions/     │  │
│  │ HUD Input │                      │  system.py    │  │
│  │ /input    │                      │  apps.py      │  │
│  └───────────┘                      │  utility.py   │  │
│                                     │  logic.py     │  │
│  ┌──────────┐                       │  games.py     │  │
│  │ speak()  │◀──────────────────────┘               │  │
│  │ pyttsx3  │                                        │  │
│  └──────────┘                                        │  │
└─────────────────────────────────────────────────────────┘
         │
         ▼
┌────────────────────┐
│  Flask HUD Server  │  ◀── Browser: http://127.0.0.1:5000
│  hud_server.py     │
│  /state  (GET/POST)│
│  /input  (POST)    │
└────────────────────┘
```

---

## Installation

### Prerequisites
- Python 3.9 or higher
- Windows OS (some features use Windows-specific APIs — `winsound`, `pyautogui`)
- A Google Gemini API Key ([Get one free here](https://aistudio.google.com/app/apikey))

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/your-username/Mini_jarvis.git
cd Mini_jarvis
```

**2. Create a virtual environment**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**3. Install dependencies**
```powershell
pip install -r requirements.txt
```

**4. Configure your API key** (see [Configuration](#configuration))

---

## Configuration

Create a `.env` file in the project root (already present if cloned):

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

> ⚠️ **Never commit your `.env` file to version control.** Add it to `.gitignore`.

To get a free Gemini API key:
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy and paste it into your `.env` file

---

## Running Jarvis

**Activate the virtual environment (if not already active):**
```powershell
.venv\Scripts\Activate.ps1
```

**Launch Jarvis:**
```powershell
python main.py
```

On startup, Jarvis will:
1. Start the HUD server at `http://127.0.0.1:5000`
2. Launch the telemetry thread (CPU/RAM/clock sync)
3. Speak a situational greeting based on the time of day
4. Begin listening for your typed commands

---

## How to Use

Jarvis runs in **Text Input Mode** — no microphone required.

### Option 1 — Terminal Prompt
When the script is running in an interactive terminal, a prompt appears:
```
──────────────────────────────────────────────────
  ⌨  TYPE YOUR COMMAND (or use the HUD browser):
──────────────────────────────────────────────────
  > what's the time?
```
Type your command and press **Enter**.

### Option 2 — HUD Browser (Recommended)
Open your browser and navigate to:
```
http://127.0.0.1:5000
```
A sci-fi HUD dashboard will appear. Use the **command input bar at the bottom** of the screen — type your command and press **Enter** or click **SEND**.

> ✅ Jarvis will always **speak the response aloud** via TTS, regardless of which input method you use.

---

## Command Reference

Jarvis understands natural language. You don't need to memorize exact phrases — just say what you mean.

| Example Command | Intent | What Happens |
|---|---|---|
| `What time is it?` | TIME | Speaks the current time |
| `What's today's date?` | DATE | Speaks today's date |
| `Tell me about black holes` | WIKIPEDIA | Fetches and reads a Wikipedia summary |
| `Open Notepad` | APP_OPEN | Launches Notepad |
| `Close Spotify` | APP_CLOSE | Terminates the Spotify process |
| `Take a screenshot` | SCREENSHOT | Saves a timestamped PNG screenshot |
| `Volume up` | VOLUME | Increases system volume |
| `Mute` | VOLUME | Toggles mute |
| `How's my CPU doing?` | HARDWARE | Reports CPU %, RAM %, Battery % |
| `Give me the latest news` | NEWS | Reads recent headlines |
| `Note down: buy groceries` | NOTE | Saves the note to a local file |
| `What's 15 times 47?` | MATH | Calculates and speaks the answer |
| `Convert 100 km to miles` | MATH | Converts and speaks the result |
| `Set an alarm for 10 minutes` | ALARM | Beeps and speaks after 10 minutes |
| `What's the weather in Lagos?` | WEATHER_API | Fetches and reads current weather |
| `Let's play rock paper scissors` | MINI_GAME | Plays an interactive RPS game |
| `Flip a coin` | MINI_GAME | Randomly speaks heads or tails |
| `Roll a dice` | MINI_GAME | Randomly speaks a dice result |
| `Shutdown the PC` | SYSTEM | Initiates Windows shutdown |
| `How are you?` | CONVERSATION | Full AI conversation via Gemini |
| `Exit` / `Goodbye` / `Shut up` | SHUT_UP | Speaks a farewell and exits |

---

## Modules

### `main.py`
The entry point and orchestration layer. Starts the HUD server, launches telemetry, delivers the startup greeting, and runs the main command loop with intent-based routing.

### `brain.py`
Integrates with **Google Gemini 2.0 Flash**. Contains:
- `classify_intent(query)` — Uses Gemini to parse a command into a structured `{ intent, parameter }` JSON object
- `get_ai_response(query)` — Sends conversational messages through a persistent chat session with full JARVIS personality
- **JARVIS Personality Prompt** — Dry, witty British demeanor; ultra-concise; sparing use of "Sir/Master"; unflappable under errors

### `engine.py`
The I/O layer:
- `speak(text)` — Converts text to speech using pyttsx3 (David/masculine voice, rate 145 WPM)
- `listen()` — Accepts typed input from terminal or HUD browser via a shared thread-safe queue
- `push_hud_input(text)` — Called by `hud_server` to inject browser commands into the listen queue

### `hud_server.py`
A Flask web server with three routes:
- `GET /` — Serves the HUD dashboard HTML
- `GET/POST /state` — Reads or updates the global Jarvis state (status, text, CPU, RAM, time, weather)
- `POST /input` — Receives commands from the browser UI and queues them for `listen()`

### `actions/system.py`
- `take_screenshot()` — Saves a timestamped PNG via pyautogui
- `control_volume(action)` — Volume up/down/mute via keyboard simulation
- `get_hardware_stats()` — CPU, RAM, battery via psutil
- `system_state(action)` — Shutdown/restart/sleep via OS commands
- `set_alarm(time_string)` — Background thread alarm with `winsound.Beep`

### `actions/apps.py`
- `open_app(name)` — Opens common applications by name
- `close_app(name)` — Finds and terminates processes by name via psutil

### `actions/utility.py`
- Time, date, Wikipedia search, news headlines, weather API, save notes

### `actions/logic.py`
- `calculate(expression)` — Safe arithmetic evaluation
- `convert_units(query)` — Common unit conversions (km↔miles, kg↔lbs, etc.)

### `actions/games.py`
- `play_mini_game(type, choice)` — Rock-Paper-Scissors, coin flip, dice roll

---

## HUD Dashboard

The visual HUD runs at `http://127.0.0.1:5000` and displays:

| Panel | Content |
|---|---|
| **Centre** | Current Jarvis status (IDLE / LISTENING / SPEAKING / RECOGNIZING) |
| **Left Panel** | Live CPU % and RAM % |
| **Right Panel** | Current time and system weather/status |
| **Bottom Transcript** | Last spoken text or processing state |
| **Command Bar** | Text input field for submitting commands from the browser |

The HUD auto-polls `/state` every second to reflect real-time system changes.

---

## Offline Mode

If no `GEMINI_API_KEY` is set, or if the API is unreachable, Jarvis falls back to **local standby protocols**:

- Greetings and identity questions are handled locally
- Jarvis informs you that cloud access is unavailable with in-character JARVIS wit
- Time, alarms, screenshots, volume, and hardware stats continue to work (no internet needed)
- Conversational and Wikipedia responses will be unavailable

---

## Troubleshooting

### Jarvis doesn't speak
- Ensure `pyttsx3` is installed: `pip install pyttsx3`
- On Windows, check that a SAPI5 voice is available (David/Zira) in Windows speech settings

### HUD doesn't load
- Confirm Flask is installed: `pip install flask`
- Make sure port 5000 is not in use by another application
- Navigate to `http://127.0.0.1:5000` (not `localhost:5000` if DNS issues exist)

### Gemini API errors
- Verify `GEMINI_API_KEY` is correctly set in `.env`
- Check your API quota at [Google AI Studio](https://aistudio.google.com/)
- Jarvis will fall back to offline mode automatically

### Commands not processing from the browser
- Ensure Jarvis (`main.py`) is actively running — the `/input` endpoint only works while the Python process is alive
- Check browser console for any `fetch` errors

---

## Dependencies

```
google-generativeai    # Gemini AI API client
python-dotenv          # .env file loading
requests               # HTTP requests (HUD state sync)
psutil                 # CPU, RAM, battery monitoring
wikipedia              # Wikipedia search
pyttsx3                # Text-to-Speech engine
Flask                  # HUD web server
pyautogui              # Screenshots & keyboard simulation
winsound               # Alarm beep (Windows only)
```

Install all at once:
```powershell
pip install -r requirements.txt
```

---

## License

This project is for personal use and educational purposes. Inspired by Marvel's Iron Man JARVIS — built with 💙 and caffeine.

---

> *"I seem to have encountered a critical error processing that request, sir. Shall we try again?"*  
> — JARVIS, on a bad day

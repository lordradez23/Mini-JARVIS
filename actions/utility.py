import datetime
import requests

def get_time():
    """Returns the current time formatted nicely."""
    return datetime.datetime.now().strftime("%I:%M %p")

def get_date():
    """Returns current date and day of the week."""
    return datetime.datetime.now().strftime("%A, %B %d, %Y")

def get_countdown(target_date_str):
    """Returns days remaining to a specific date."""
    try:
        target = datetime.datetime.strptime(target_date_str, "%Y-%m-%d")
        now = datetime.datetime.now()
        diff = target - now
        if diff.days < 0:
            return "That date has already passed, master."
        return f"There are {diff.days} days remaining until {target_date_str}."
    except:
        return "I couldn't calculate that. Please use YYYY-MM-DD format."

def save_note(text):
    """Saves a voice note to a text file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("notes.txt", "a") as f:
        f.write(f"[{timestamp}] {text}\n")
    return "I've saved that note for you, master."

def get_news():
    """Fetches top news headlines."""
    try:
        url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=e63968600d3e42ea9f8997f8997f89ef"
        response = requests.get(url).json()
        articles = response.get('articles', [])[:3]
        headlines = [a['title'] for a in articles]
        return "Top headlines: " + ". ".join(headlines)
    except:
        return "I'm having trouble connecting to the news network."

def get_weather(location):
    """Fetches real-time weather."""
    try:
        url = f"https://wttr.in/{location}?format=3"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return f"The current weather in {location} is {response.text.strip()}."
        return f"I couldn't retrieve the weather for {location}."
    except:
        return f"I encountered an error connecting to the weather service."

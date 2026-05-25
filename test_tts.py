import pyttsx3
import time

def test_tts():
    print("Initializing TTS engine...")
    try:
        engine = pyttsx3.init()
        print("Engine initialized.")
        
        voices = engine.getProperty('voices')
        print(f"Number of voices found: {len(voices)}")
        
        text = "Hello Anointed, this is a test of the emergency broadcast system."
        print(f"Saying: {text}")
        engine.say(text)
        print("Waiting for completion...")
        engine.runAndWait()
        print("TTS test completed.")
    except Exception as e:
        print(f"TTS Test Error: {e}")

if __name__ == "__main__":
    test_tts()

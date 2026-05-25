import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GEMINI_API_KEY")
print(f"Testing Key: {key[:5]}...{key[-5:]}")

genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-1.5-flash')

try:
    print("Sending test message...")
    response = model.generate_content("Hello, act as JARVIS and say 'Systems Online'.")
    print(f"API Response: {response.text}")
except Exception as e:
    print(f"DIAGNOSTIC FAILED: {e}")

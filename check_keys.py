import os
from dotenv import load_dotenv

load_dotenv()

print("--- ENV DIAGNOSTIC ---")
for key in os.environ:
    if "KEY" in key or "GEMINI" in key or "GOOGLE" in key:
        val = os.environ[key]
        if len(val) > 10:
            masked = val[:5] + "..." + val[-5:]
            print(f"{key}: {masked}")
        else:
            print(f"{key}: {val}")

if os.path.exists(".env"):
    print("\n--- .env FILE ---")
    with open(".env", "r") as f:
        for line in f:
            if "GEMINI_API_KEY" in line:
                print(f"Detected: {line.strip()[:20]}...")

import sounddevice as sd
import numpy as np
import time

def test_playback():
    fs = 44100
    seconds = 3
    
    print(f"--- MIC PLAYBACK TEST ---")
    print(f"Recording for {seconds} seconds... Speak into your mic!")
    
    try:
        # Get defaults
        device_info = sd.query_devices(kind='input')
        print(f"Using device: {device_info['name']}")
        
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='float32')
        sd.wait()
        
        print("Recording finished. Playing back...")
        sd.play(myrecording, fs)
        sd.wait()
        print("Playback finished.")
        
        max_amp = np.max(np.abs(myrecording))
        print(f"Max Amplitude detected: {max_amp:.5f}")
        
        if max_amp < 0.001:
            print("\n❌ RESULT: I can't hear anything. Check your Windows Sound Settings to see if the mic is enabled/active.")
        else:
            print("\n✅ RESULT: Audio is working! The problem is likely in the recognition layer.")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_playback()

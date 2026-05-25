import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import os

def check_audio():
    print("--- Audio Hardware Diagnostic ---")
    try:
        device_info = sd.query_devices(kind='input')
        print(f"Default Input Device: {device_info['name']}")
        print(f"Default Sample Rate: {device_info['default_samplerate']}")
        print(f"Max Input Channels: {device_info['max_input_channels']}")
        
        fs = int(device_info['default_samplerate'])
        seconds = 3
        
        print(f"\nRecording {seconds} seconds for diagnostic...")
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        
        # Calculate signal strength
        rms = np.sqrt(np.mean(myrecording**2))
        max_amp = np.max(np.abs(myrecording))
        
        print(f"\n--- Results ---")
        print(f"RMS Amplitude: {rms:.2f}")
        print(f"Peak Amplitude: {max_amp}")
        
        if max_amp < 100:
            print("⚠️ WARNING: Very low signal detected. Is your mic muted or very quiet?")
        elif max_amp > 30000:
            print("⚠️ WARNING: Signal clipping detected. Your mic might be too loud.")
        else:
            print("✅ Signal levels look okay.")
            
        # Save to file for verification
        wav.write("diagnostic_test.wav", fs, myrecording)
        print(f"Saved diagnostic recording to 'diagnostic_test.wav'")
        
    except Exception as e:
        print(f"❌ Error during diagnostic: {e}")

if __name__ == "__main__":
    check_audio()

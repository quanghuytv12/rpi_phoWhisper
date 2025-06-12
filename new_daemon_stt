import numpy as np
from transformers import pipeline
import time
import os
from daemon_audio import audio_queue

# Configuration
PHOWHISPER_MODEL = "models/phowhisper"  # Path to PhoWhisper checkpoint
TRANSCRIPTION_DIR = "data/transcriptions"

# Initialize STT
try:
    stt = pipeline("automatic-speech-recognition", model=PHOWHISPER_MODEL, device=-1)  # CPU
except Exception as e:
    print(f"Failed to load PhoWhisper model: {e}")
    exit(1)

# Ensure transcription directory exists
os.makedirs(TRANSCRIPTION_DIR, exist_ok=True)

def main():
    print("Starting STT daemon...")
    while True:
        try:
            # Get audio from queue
            audio_data = audio_queue.get(timeout=1.0)
            
            # Convert to float32 for STT
            audio_float = audio_data.astype(np.float32) / 32768.0
            
            # Speech-to-Text
            start_time = time.time()
            transcription = stt(audio_float, return_timestamps=False)["text"].strip()
            latency = time.time() - start_time
            print(f"Transcription: {transcription} (Latency: {latency:.2f}s)")
            
            # Save transcription
            if transcription:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                with open(f"{TRANSCRIPTION_DIR}/{timestamp}.txt", "w") as f:
                    f.write(transcription)
                print(f"Transcription saved: {TRANSCRIPTION_DIR}/{timestamp}.txt")
            
        except queue.Empty:
            continue
        except KeyboardInterrupt:
            print("Stopping STT daemon...")
            break
        except Exception as e:
            print(f"STT error: {e}")
            continue

if __name__ == "__main__":
    main()

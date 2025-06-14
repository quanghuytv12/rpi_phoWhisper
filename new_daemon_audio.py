import pyaudio
import numpy as np
import pvporcupine
import time
import os
import queue
import threading
from scipy.signal import get_window

# Configuration
DEVICE_INDEX = 1
SAMPLE_RATE = 16000  # Porcupine requires 16kHz
FRAME_LENGTH = 512   # Porcupine frame length
BUFFER_SECONDS = 5
PRE_BUFFER_SECONDS = 1
SILENCE_THRESHOLD = 0.01  # Energy threshold for silence detection
SILENCE_DURATION = 1.0    # Seconds of silence to stop recording
ACCESS_KEY = "YOUR_PICOVOICE_ACCESS_KEY"  # Replace with your Picovoice AccessKey
WAKEWORD = "jarvis"  # Or custom wake word
WAKEWORD_MODEL_PATH = "models/hey_jarvis.ppn"  # Adjust path relative to repo

# Shared queue for audio data
audio_queue = queue.Queue()

# Initialize PyAudio
pa = pyaudio.PyAudio()

# List audio devices for debugging
def list_audio_devices():
    print("Available audio devices:")
    for i in range(pa.get_device_count()):
        device_info = pa.get_device_info_by_index(i)
        print(f"Index {i}: {device_info['name']}, Input Channels: {device_info['maxInputChannels']}")

list_audio_devices()

stream = pa.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=SAMPLE_RATE,
    input=True,
    frames_per_buffer=FRAME_LENGTH,
    input_device_index=DEVICE_INDEX
)

# Initialize Porcupine
try:
    porcupine = pvporcupine.create(
        access_key=ACCESS_KEY,
        keywords=[WAKEWORD],
        model_path=WAKEWORD_MODEL_PATH if os.path.exists(WAKEWORD_MODEL_PATH) else None,
        sensitivities=[0.8]  # Increase sensitivity
    )
except Exception as e:
    print(f"Failed to initialize Porcupine: {e}")
    stream.close()
    pa.terminate()
    exit(1)

# Buffer
buffer = np.zeros(int(SAMPLE_RATE * BUFFER_SECONDS), dtype=np.int16)
pre_buffer = np.zeros(int(SAMPLE_RATE * PRE_BUFFER_SECONDS), dtype=np.int16)

def detect_silence(audio_data, threshold=SILENCE_THRESHOLD):
    """Detect silence based on energy threshold"""
    window = get_window("hann", len(audio_data))
    energy = np.sum((audio_data.astype(np.float32) / 32768.0) ** 2 * window)
    return energy < threshold

def audio_processing():
    recording = False
    silence_start = None
    full_audio = []
    
    while True:
        try:
            data = np.frombuffer(stream.read(porcupine.frame_length, exception_on_overflow=False), dtype=np.int16)
            
            if not recording:
                # Update buffers
                buffer = np.roll(buffer, -len(data))
                buffer[-len(data):] = data
                pre_buffer = np.roll(pre_buffer, -len(data))
                pre_buffer[-len(data):] = data
                
                # Detect wake word
                keyword_index = porcupine.process(data)
                if keyword_index >= 0:
                    print(f"Detected wake word: {WAKEWORD}")
                    recording = True
                    full_audio = list(pre_buffer) + list(buffer)
                    # Save debug WAV
                    import sounddevice as sd
                    sd.write_wav("data/audio_chunks/debug_audio.wav", np.array(full_audio), SAMPLE_RATE)
            else:
                # Continue recording until silence
                full_audio.extend(data)
                if detect_silence(data):
                    if silence_start is None:
                        silence_start = time.time()
                    elif time.time() - silence_start > SILENCE_DURATION:
                        # Send audio to queue
                        audio_queue.put(np.array(full_audio, dtype=np.int16))
                        print("Audio segment sent to queue")
                        recording = False
                        full_audio = []
                        silence_start = None
                else:
                    silence_start = None
                
        except Exception as e:
            print(f"Audio processing error: {e}")

def main():
    # Start audio thread
    audio_thread = threading.Thread(target=audio_processing)
    audio_thread.daemon = True  # Run as daemon
    audio_thread.start()
    
    print(f"Audio daemon started, listening for '{WAKEWORD}'...")
    try:
        while True:
            time.sleep(1)  # Keep daemon running
    except KeyboardInterrupt:
        print("Stopping audio daemon...")
        porcupine.delete()
        stream.stop_stream()
        stream.close()
        pa.terminate()

if __name__ == "__main__":
    main()

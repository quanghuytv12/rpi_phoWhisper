import pyaudio, wave, time, os

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 10
OUTPUT_DIR = "data/audio_chunks"

def record_chunk():
    pa = pyaudio.PyAudio()
    stream = pa.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = [stream.read(CHUNK) for _ in range(int(RATE/CHUNK*RECORD_SECONDS))]
    stream.stop_stream(); stream.close(); pa.terminate()
    return frames

def save_chunk(frames, path):
    wf = wave.open(path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames)); wf.close()

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    while True:
        ts = time.strftime("%Y%m%d-%H%M%S")
        fp = os.path.join(OUTPUT_DIR, f"audio_{ts}.wav")
        save_chunk(record_chunk(), fp)
        print(f"✔️  Saved {fp}")

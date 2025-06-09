import os, time
import torchaudio
from transformers import WhisperForConditionalGeneration, WhisperProcessor

MODEL_PATH = "models/phowhisper"
AUDIO_DIR = "data/audio_chunks"
TXT_DIR = "data/transcriptions"

model = WhisperForConditionalGeneration.from_pretrained(MODEL_PATH)
processor = WhisperProcessor.from_pretrained(MODEL_PATH)

def transcribe(wav_path):
    wav, sr = torchaudio.load(wav_path)
    inputs = processor(wav.squeeze().numpy(), sampling_rate=sr, return_tensors="pt").input_features
    ids = model.generate(inputs)
    return processor.batch_decode(ids, skip_special_tokens=True)[0]

if __name__ == "__main__":
    os.makedirs(TXT_DIR, exist_ok=True)
    while True:
        for f in os.listdir(AUDIO_DIR):
            if not f.endswith(".wav"): continue
            src = os.path.join(AUDIO_DIR, f)
            text = transcribe(src)
            dst = os.path.join(TXT_DIR, f.replace(".wav", ".txt"))
            with open(dst, "w") as out: out.write(text)
            os.remove(src)
            print(f"✔️  Transcribed → {dst}")
        time.sleep(1)

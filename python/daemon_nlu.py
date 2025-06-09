import os 
import time
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_PATH = "models/phobert"
TXT_DIR = "data/transcriptions"
OUT_DIR = "data/nlu_results"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model     = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

def predict(text):
    inp = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    logits = model(**inp).logits
    return logits.argmax(dim=-1).item()

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    while True:
        for f in os.listdir(TXT_DIR):
            if not f.endswith(".txt"): continue
            path = os.path.join(TXT_DIR, f)
            with open(path) as r: txt = r.read()
            cls = predict(txt)
            out = os.path.join(OUT_DIR, f.replace(".txt", "_nlu.txt"))
            with open(out, "w") as w: w.write(str(cls))
            os.remove(path)
            print(f"✔️  NLU → {out}")
        time.sleep(1)

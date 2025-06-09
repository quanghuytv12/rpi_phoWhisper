# rpi\_phoWhisper

A lightweight pipeline on Raspberry Pi 5 for recording audio, transcribing with a custom PhoWhisper model, and (optionally) processing transcriptions via a PhoBERT NLU model.

---

## 📖 Overview

This repository provides scripts to:

1. **Record audio** in continuous 10‑second WAV chunks via a USB microphone.
2. **Transcribe** each chunk to text using a custom-finetuned PhoWhisper model.
3. **(Optional)** Perform NLU (e.g., intent classification) using a custom-finetuned PhoBERT model.
4. **Run as daemons** for continuous operation, or test manually step-by-step.

Designed for ease of use: clone, configure a Python virtual environment, install dependencies, and run.

---

## 🚀 Prerequisites

* **Hardware**: Raspberry Pi 5 (16 GB RAM) with USB microphone.
* **OS**: Raspberry Pi OS (64‑bit).
* **Python**: 3.11 (installed via system).
* **Git**: for cloning the repo.

---

## 📂 Repository Structure

```plaintext
rpi_phoWhisper/
├─ .gitignore
├─ README.md
├─ run.sh
├─ system/
│  └─ install.sh
├─ python/
│  ├─ daemon_audio.py
│  ├─ daemon_stt.py
│  └─ daemon_nlu.py
├─ models/
│  ├─ phowhisper/    ← custom PhoWhisper model files
│  └─ phobert/       ← (optional) custom PhoBERT model files
├─ data/             ← automatically created
│  ├─ audio_chunks/
│  ├─ transcriptions/
│  └─ nlu_results/
└─ venv/             ← Python virtual environment
```

---

## ⚙️ Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/quanghuytv12/rpi_phoWhisper.git
   cd rpi_phoWhisper
   ```

2. **Create & activate a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   bash system/install.sh
   ```

   This will:

   * install system packages (`portaudio19-dev`, etc.)
   * install Python libraries (`torch`, `torchaudio`, `transformers`, `pyaudio`)
   * create `data/` subfolders

4. **Verify data directories**:

   ```bash
   ls data
   # → audio_chunks  transcriptions  nlu_results
   ```

5. **Add custom models**:

   * Copy your PhoWhisper model to `models/phowhisper/`.
   * (Optional) Copy your PhoBERT model to `models/phobert/`.

6. **Configure microphone device** (if needed):

   * List audio devices:

     ```bash
     arecord -l
     ```
   * Edit `python/daemon_audio.py`, set `DEVICE_INDEX` to your USB mic index:

     ```python
     DEVICE_INDEX = 1
     ```

---

## ▶️ Usage

### 1. Audio → STT only

Run just recording and transcription:

```bash
# ensure venv is active
source venv/bin/activate
# start audio & STT daemons
bash run.sh  # remove or comment out daemon_nlu.py line
```

### 2. Manual step-by-step

* **Record one chunk**:

  ```bash
  python3 python/daemon_audio.py
  # press Ctrl+C after one file saves
  ```
* **Transcribe that chunk**:

  ```bash
  python3 python/daemon_stt.py
  ```
* **View transcription**:

  ```bash
  cat data/transcriptions/*.txt
  ```

### 3. Full pipeline (including NLU)

After adding PhoBERT model:

```bash
source venv/bin/activate
python3 python/daemon_audio.py &
python3 python/daemon_stt.py &
python3 python/daemon_nlu.py &
echo "All daemons running"
```

## 🤝 Contributing

Feel free to open issues or pull requests for improvements (logging, Docker, systemd services, etc.).

---

## 📄 License

MIT License. See [LICENSE](LICENSE) if provided.

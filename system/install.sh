#!/bin/bash
set -e

# 1. Cập nhật hệ thống
sudo apt update && sudo apt upgrade -y

# 2. Cài gói hệ thống cho âm thanh
sudo apt install -y python3-pip python3-venv portaudio19-dev

# 3. Tạo venv trong thư mục project
python3 -m venv venv

# 4. Kích hoạt venv và cài Python deps
source venv/bin/activate
pip install --upgrade pip
pip install torch torchaudio transformers pyaudio

# 5. Tạo thư mục dữ liệu
mkdir -p /data/audio_chunks /data/transcriptions /data/nlu_results
sudo chown -R $USER /data

echo "✔️  Installation complete. Remember to 'source venv/bin/activate' before running."

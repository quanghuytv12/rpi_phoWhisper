#!/bin/bash
# Install system packages
sudo apt-get update
sudo apt-get install -y portaudio19-dev

# Install Python dependencies
pip install pvporcupine transformers torch torchaudio scipy sounddevice

# Create data directories
mkdir -p data/audio_chunks data/transcriptions data/nlu_results

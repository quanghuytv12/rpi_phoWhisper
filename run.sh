#!/bin/bash
set -e
# 1. Source venv
source "$(dirname "$0")/venv/bin/activate"

# 2. Khởi chạy các daemon
python3 python/daemon_audio.py &
python3 python/daemon_stt.py &

echo "🎤 Running audio + STT only (NLU skipped)"
# python3 python/daemon_nlu.py &

# echo "✔️  All daemons started under virtualenv."

#!/data/data/com.termux/files/usr/bin/bash
set -e
cd "$(dirname "$0")"

if command -v pkg >/dev/null 2>&1; then
  pkg install -y python mpv ffmpeg >/dev/null 2>&1 || true
fi

python - <<'PY'
import importlib.util, subprocess, sys
mods = {"rich":"rich", "requests":"requests", "psutil":"psutil", "yt_dlp":"yt-dlp"}
missing = [pkg for mod,pkg in mods.items() if importlib.util.find_spec(mod) is None]
if missing:
    print("Installing missing Python packages:", ", ".join(missing))
    subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
PY

[ -f .env ] || cp .env.example .env
exec python app.py

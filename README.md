# Tools-private

## Install Termux

```bash
pkg update -y
pkg upgrade -y
pkg install -y git python mpv ffmpeg
```

## Clone

```bash
cd ~
git clone https://github.com/DenzCoder/Tools-private.git
cd Tools-private
```

## Install Python packages

```bash
python -m pip install -r requirements.txt
```

## Setup

```bash
cp .env.example .env
```

## Run

```bash
python app.py
```

Atau gunakan launcher:

```bash
chmod +x run.sh
./run.sh
```

## Update

Kalau ada update dari GitHub:

```bash
cd ~/Tools-private
git pull
python app.py
```

## Troubleshooting

Jika Python atau package belum tersedia:

```bash
pkg update -y
pkg install -y python git mpv ffmpeg
python -m pip install -r requirements.txt
python app.py
```

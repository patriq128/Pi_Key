#!/bin/bash

set -e

REPO="https://raw.githubusercontent.com/patriq128/Pi_Key/main"

APP="app.py"
REQ="requirements.txt"

echo "== Pi_Key Smart Installer =="

# ----------------------------
# INPUT SAFE MODE
# ----------------------------
ANS="${1:-}"

if [ -z "$ANS" ]; then
    if [ -t 0 ]; then
        read -p "Continue installation? (y/n): " ANS
    else
        ANS="y"
    fi
fi

case "$ANS" in
    y|Y|yes|YES)
        echo "Continuing..."
        ;;
    *)
        echo "Cancelled."
        exit 0
        ;;
esac

# ----------------------------
# OS DETECTION
# ----------------------------
OS="$(uname -s)"

echo "[1/6] Detecting system..."

if [[ "$OS" == "Linux" ]]; then
    PLATFORM="linux"
elif [[ "$OS" == "Darwin" ]]; then
    PLATFORM="mac"
else
    echo "Unsupported OS: $OS"
    exit 1
fi

echo "Platform: $PLATFORM"

# ----------------------------
# PYTHON DETECTION
# ----------------------------
echo "[2/6] Checking Python..."

if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo "Python not found. Installing..."

    if [[ "$PLATFORM" == "linux" ]]; then
        if command -v apt &>/dev/null; then
            sudo apt update && sudo apt install -y python3 python3-venv python3-pip
        elif command -v dnf &>/dev/null; then
            sudo dnf install -y python3 python3-pip
        elif command -v pacman &>/dev/null; then
            sudo pacman -S python python-pip --noconfirm
        fi
    elif [[ "$PLATFORM" == "mac" ]]; then
        if ! command -v brew &>/dev/null; then
            echo "Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew install python
    fi
fi

echo "Using: $($PYTHON --version)"

# ----------------------------
# DOWNLOAD FILES
# ----------------------------
echo "[3/6] Downloading files..."

curl -fsSL "$REPO/$APP" -o "$APP"
curl -fsSL "$REPO/$REQ" -o "$REQ" || echo "No requirements.txt found"

# ----------------------------
# VENV AUTO DETECT FIX (PEP 668 SAFE)
# ----------------------------
echo "[4/6] Setting up environment..."

VENV_DIR="venv"

$PYTHON -m venv $VENV_DIR

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

echo "Virtual environment activated."

# ----------------------------
# PIP INSTALL INSIDE VENV
# ----------------------------
echo "[5/6] Installing dependencies..."

pip install --upgrade pip

if [ -f "$REQ" ]; then
    pip install -r "$REQ"
fi

# ----------------------------
# RUN APP
# ----------------------------
echo "[6/6] Starting Pi_Key..."

if [ -t 0 ]; then
    python app.py
else
    python -u app.py < /dev/tty
fi

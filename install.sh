#!/bin/bash

set -e

REPO="https://raw.githubusercontent.com/patriq128/Pi_Key/main"

APP="app.py"
REQ="requirements.txt"

echo "== Pi_Key Installer =="

read -p "Continue installation? (y/n): " ans
if [[ "$ans" != "y" ]]; then
    echo "Cancelled."
    exit 0
fi

# Detect OS
OS="$(uname -s)"

echo "[1/5] Checking Python..."

if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo "Python not found."

    if [[ "$OS" == "Linux" ]]; then
        echo "Installing Python via package manager..."
        if command -v apt &>/dev/null; then
            sudo apt update && sudo apt install -y python3 python3-pip
        elif command -v dnf &>/dev/null; then
            sudo dnf install -y python3 python3-pip
        elif command -v pacman &>/dev/null; then
            sudo pacman -S python python-pip --noconfirm
        fi
    elif [[ "$OS" == "Darwin" ]]; then
        echo "Installing Python via Homebrew..."
        if ! command -v brew &>/dev/null; then
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew install python
    fi

    if command -v python3 &>/dev/null; then
        PYTHON=python3
    else
        PYTHON=python
    fi
fi

echo "Using: $($PYTHON --version)"

echo "[2/5] Updating pip..."
$PYTHON -m ensurepip --upgrade || true
$PYTHON -m pip install --upgrade pip || true

echo "[3/5] Downloading project files..."

curl -L "$REPO/$APP" -o "$APP"
curl -L "$REPO/$REQ" -o "$REQ" || echo "No requirements.txt found"

echo "[4/5] Installing dependencies..."

if [ -f "$REQ" ]; then
    $PYTHON -m pip install -r "$REQ"
fi

echo "[5/5] Launching Pi_Key..."

$PYTHON $APP
#!/bin/bash

set -e

REPO="https://raw.githubusercontent.com/patriq128/Pi_Key/main"

APP="app.py"
REQ="requirements.txt"

echo "== Pi_Key Installer =="

# ----------------------------
# Safe input handling (IMPORTANT FIX)
# ----------------------------

ANS="${1:-}"

if [ -z "$ANS" ]; then
    if [ -t 0 ]; then
        read -p "Continue installation? (y/n): " ANS
    else
        ANS="y"
        echo "Non-interactive mode detected → auto-continue"
    fi
fi

if [[ "$ANS" != "y" ]]; then
    echo "Cancelled."
    exit 0
fi

# ----------------------------
# OS detect
# ----------------------------
OS="$(uname -s)"

echo "[1/5] Checking Python..."

if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo "Python not found. Installing..."

    if [[ "$OS" == "Linux" ]]; then
        if command -v apt &>/dev/null; then
            sudo apt update && sudo apt install -y python3 python3-pip
        elif command -v dnf &>/dev/null; then
            sudo dnf install -y python3 python3-pip
        elif command -v pacman &>/dev/null; then
            sudo pacman -S python python-pip --noconfirm
        else
            echo "Unsupported Linux package manager"
            exit 1
        fi

    elif [[ "$OS" == "Darwin" ]]; then
        if ! command -v brew &>/dev/null; then
            echo "Installing Homebrew..."
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

# ----------------------------
# pip setup
# ----------------------------
echo "[2/5] Updating pip..."
$PYTHON -m ensurepip --upgrade || true
$PYTHON -m pip install --upgrade pip || true

# ----------------------------
# Download project
# ----------------------------
echo "[3/5] Downloading files..."

curl -fsSL "$REPO/$APP" -o "$APP"
curl -fsSL "$REPO/$REQ" -o "$REQ" || echo "No requirements.txt found"

# ----------------------------
# Install dependencies
# ----------------------------
echo "[4/5] Installing dependencies..."

if [ -f "$REQ" ]; then
    $PYTHON -m pip install -r "$REQ"
fi

# ----------------------------
# Run app
# ----------------------------
echo "[5/5] Starting Pi_Key..."

$PYTHON $APP

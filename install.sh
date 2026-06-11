#!/bin/bash

set -e

REPO="https://raw.githubusercontent.com/patriq128/Pi_Key/main"

APP="app.py"
REQ="requirements.txt"

echo "== Pi_Key Installer =="

# ----------------------------
# CONFIRMATION
# ----------------------------

if [ -e /dev/tty ]; then
    read -p "Continue installation? (y/n): " ANS < /dev/tty
else
    echo "No interactive terminal found."
    exit 1
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

if [[ "$OS" == "Linux" ]]; then
    PLATFORM="linux"
elif [[ "$OS" == "Darwin" ]]; then
    PLATFORM="macOS"
else
    echo "Unsupported operating system: $OS"
    exit 1
fi

echo "[1/5] Detected platform: $PLATFORM"

# ----------------------------
# PYTHON DETECTION
# ----------------------------

echo "[2/5] Checking Python..."

if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
elif command -v python >/dev/null 2>&1; then
    PYTHON=python
else
    echo "Python not found."

    if [[ "$PLATFORM" == "linux" ]]; then

        if command -v apt >/dev/null 2>&1; then
            sudo apt update
            sudo apt install -y python3 python3-venv python3-pip

        elif command -v dnf >/dev/null 2>&1; then
            sudo dnf install -y python3 python3-pip

        elif command -v pacman >/dev/null 2>&1; then
            sudo pacman -S --noconfirm python python-pip

        else
            echo "Unsupported package manager."
            exit 1
        fi

    elif [[ "$PLATFORM" == "macOS" ]]; then

        if ! command -v brew >/dev/null 2>&1; then
            echo "Installing Homebrew..."

            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi

        brew install python
    fi

    PYTHON=python3
fi

echo "Using: $($PYTHON --version)"

# ----------------------------
# DOWNLOAD FILES
# ----------------------------

echo "[3/5] Downloading files..."

curl -fsSL "$REPO/$APP" -o "$APP"

if curl -fsSL "$REPO/$REQ" -o "$REQ"; then
    echo "requirements.txt downloaded."
else
    echo "requirements.txt not found."
fi


# ----------------------------
# INSTALL DEPENDENCIES
# ----------------------------

echo "[4/5] Installing dependencies..."

python -m pip install --upgrade pip

if [ -f "$REQ" ]; then
    pip install -r "$REQ --break-system-packages"
fi

# ----------------------------
# START APPLICATION
# ----------------------------

echo "[5/5] Starting Pi_Key..."

if [ -e /dev/tty ]; then
    python "$APP" < /dev/tty
else
    python "$APP"
fi

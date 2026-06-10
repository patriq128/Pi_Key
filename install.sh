#!/bin/bash

set -e

REPO="https://raw.githubusercontent.com/patriq128/Pi_Key/main"

APP="app.py"
REQ="requirements.txt"

echo "== Pi_Key Installer =="

# ----------------------------
# FIXED INPUT HANDLING
# ----------------------------

ANS="${1:-}"

# FORCE PIPE SAFETY FIX
if [ -z "$ANS" ] || [ "$ANS" = " " ]; then
    if [ -t 0 ]; then
        read -p "Continue installation? (y/n): " ANS
    else
        ANS="y"
    fi
fi

echo "DEBUG ANS = '$ANS'"

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
        fi

    elif [[ "$OS" == "Darwin" ]]; then
        if ! command -v brew &>/dev/null; then
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew install python
    fi

    PYTHON=python3
fi

echo "Using: $($PYTHON --version)"

# ----------------------------
# pip
# ----------------------------
$PYTHON -m ensurepip --upgrade || true
$PYTHON -m pip install --upgrade pip || true

# ----------------------------
# download
# ----------------------------
curl -fsSL "$REPO/$APP" -o "$APP"
curl -fsSL "$REPO/$REQ" -o "$REQ" || echo "No requirements.txt"

# ----------------------------
# install deps
# ----------------------------
if [ -f "$REQ" ]; then
    $PYTHON -m pip install -r "$REQ"
fi

# ----------------------------
# run
# ----------------------------
$PYTHON $APP

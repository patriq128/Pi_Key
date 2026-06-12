$ErrorActionPreference = "Stop"

$Repo = "https://raw.githubusercontent.com/patriq128/Pi_Key/main"

$App = "app.py"
$Req = "requirements.txt"

Write-Host "== Pi_Key Installer =="

# ----------------------------
# CONFIRMATION
# ----------------------------

$Answer = Read-Host "Continue installation? (y/n)"

if ($Answer -notmatch '^(y|yes)$') {
    Write-Host "Cancelled."
    exit
}

Write-Host "Continuing..."

# ----------------------------
# PYTHON DETECTION
# ----------------------------

Write-Host "[1/4] Checking Python..."

$Python = $null

try {
    py --version | Out-Null
    $Python = "py"
}
catch {
    try {
        python --version | Out-Null
        $Python = "python"
    }
    catch {
        Write-Host "Python not found."
        Write-Host ""
        Write-Host "Download Python from:"
        Write-Host "https://www.python.org/downloads/windows/"
        exit 1
    }
}

Write-Host "Using: $(& $Python --version)"

# ----------------------------
# DOWNLOAD FILES
# ----------------------------

Write-Host "[2/4] Downloading files..."

Invoke-WebRequest `
    -Uri "$Repo/$App" `
    -OutFile $App

try {
    Invoke-WebRequest `
        -Uri "$Repo/$Req" `
        -OutFile $Req

    Write-Host "requirements.txt downloaded."
}
catch {
    Write-Host "requirements.txt not found."
}

# ----------------------------
# INSTALL DEPENDENCIES
# ----------------------------

Write-Host "[3/4] Installing dependencies..."

& $Python -m pip install --upgrade pip

if (Test-Path $Req) {
    & $Python -m pip install -r $Req
}

# ----------------------------
# START APPLICATION
# ----------------------------

Write-Host "[4/4] Starting Pi_Key..."

& $Python $App
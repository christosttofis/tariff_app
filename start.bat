@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo  CERA Tariff API - Startup
echo ============================================================
echo.

:: ── 1. Check Python ──────────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not on PATH.
    echo.
    echo         Opening the Python download page in your browser...
    echo         Install Python 3.11 or newer, tick "Add Python to PATH",
    echo         then run this script again.
    echo.
    start https://www.python.org/downloads/
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('python --version 2^>^&1') do echo [OK] %%v found

:: ── 2. Move into tariff-api ───────────────────────────────────
cd /d "%~dp0tariff-api"

:: ── 3. Create virtual environment if missing ─────────────────
if not exist ".venv\Scripts\activate.bat" (
    echo [INFO] Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created.
) else (
    echo [OK] Virtual environment already exists.
)

:: ── 4. Activate virtual environment ──────────────────────────
call .venv\Scripts\activate.bat

:: ── 5. Install / update dependencies ─────────────────────────
echo [INFO] Checking dependencies...
pip install -q --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org
pip install -q -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)
echo [OK] Dependencies up to date.

:: ── 6. Start the server ───────────────────────────────────────
echo.
echo ============================================================
echo  Server starting at http://localhost:8000
echo  Customer: http://localhost:8000/customer.html
echo  Admin:    http://localhost:8000/admin.html
echo  Admin:    http://localhost:8000/supplier.html
echo  API docs: http://localhost:8000/docs
echo  Press Ctrl+C to stop.
echo ============================================================
echo.
python -m uvicorn main:app --host 0.0.0.0 --port 8000

pause

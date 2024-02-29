@echo off

REM Set the script directory as the current directory
cd /d "%~dp0"

REM Check if .venv directory exists
if not exist .venv (
  echo Creating .venv directory...
  python -m venv .venv
  call .venv\Scripts\activate
  pip install -r requirements.txt
)

REM Activate .venv
call .venv\Scripts\activate

REM Delay for 3 seconds
timeout /t 3 /nobreak >nul

REM Start cloudflared
start "" "%~dp0start-cloudflared.bat"

REM Run main.py
python "%~dp0src\main.py"

REM Deactivate .venv
deactivate
@echo off
REM Convenience script to start the file transfer server on Windows

REM Get the directory where this script is located
cd /d "%~dp0"

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Start the server
python server.py %*


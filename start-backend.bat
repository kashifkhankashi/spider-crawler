@echo off
cd backend

REM Try to activate venv, if it fails, use system Python
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo Using virtual environment
) else (
    echo Virtual environment not found, using system Python
    echo Make sure dependencies are installed: pip install -r requirements.txt
)

echo Starting Backend Server on http://localhost:8000
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000



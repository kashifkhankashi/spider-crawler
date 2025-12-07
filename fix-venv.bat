@echo off
echo Fixing Virtual Environment Issue...
echo.

cd backend

echo Step 1: Stopping any running Python processes...
taskkill //F //IM python.exe 2>nul
taskkill //F //IM uvicorn.exe 2>nul
timeout /t 2 /nobreak >nul

echo Step 2: Removing old virtual environment...
if exist venv (
    echo Deleting venv directory...
    rmdir /s /q venv 2>nul
    if exist venv (
        echo ERROR: Could not delete venv. Please close all terminals and try again.
        echo Or delete the 'backend\venv' folder manually.
        pause
        exit /b 1
    )
    echo Old venv removed successfully!
) else (
    echo No existing venv found.
)

echo.
echo Step 3: Creating new virtual environment...
python -m venv venv
if errorlevel 1 (
    echo.
    echo ERROR: Failed to create virtual environment!
    echo.
    echo SOLUTION: You can run without venv. The setup script will handle this.
    echo Run: setup-backend-windows.bat
    pause
    exit /b 1
)

echo Virtual environment created successfully!
echo.
echo Step 4: Activating and installing dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)"

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo You can now start the backend with:
echo   start-backend.bat
echo.
pause


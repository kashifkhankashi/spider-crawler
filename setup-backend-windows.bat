@echo off
echo ========================================
echo Backend Setup for Windows
echo ========================================
echo.

cd backend

echo Step 1: Creating virtual environment...
if exist venv (
    echo Virtual environment already exists.
    echo Deleting old venv...
    rmdir /s /q venv
)

python -m venv venv
if errorlevel 1 (
    echo.
    echo ERROR: Failed to create virtual environment!
    echo.
    echo Trying alternative method...
    python -m venv venv --clear
    if errorlevel 1 (
        echo.
        echo Virtual environment creation failed.
        echo You can continue without venv (packages will be installed globally).
        echo.
        set /p continue="Continue without venv? (y/n): "
        if /i not "%continue%"=="y" (
            echo Setup cancelled.
            pause
            exit /b 1
        )
        goto :no_venv
    )
)

echo Virtual environment created successfully!
echo.

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo WARNING: Could not activate venv, using system Python
    goto :no_venv
)

:with_venv
echo Virtual environment activated.
echo.

echo Step 3: Upgrading pip...
python -m pip install --upgrade pip
echo.

echo Step 4: Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)
echo.

echo Step 5: Installing Playwright browsers...
playwright install chromium
if errorlevel 1 (
    echo WARNING: Playwright installation failed, but continuing...
)
echo.

echo Step 6: Downloading NLTK data...
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)"
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the backend server, run:
echo   start-backend.bat
echo.
echo Or manually:
echo   cd backend
echo   venv\Scripts\activate
echo   uvicorn app.main:app --reload
echo.
pause
exit /b 0

:no_venv
echo.
echo Installing packages globally (no virtual environment)...
echo.

echo Step 1: Upgrading pip...
python -m pip install --upgrade pip
echo.

echo Step 2: Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)
echo.

echo Step 3: Installing Playwright browsers...
playwright install chromium
if errorlevel 1 (
    echo WARNING: Playwright installation failed, but continuing...
)
echo.

echo Step 4: Downloading NLTK data...
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)"
echo.

echo ========================================
echo Setup Complete (without venv)!
echo ========================================
echo.
echo To start the backend server, run:
echo   start-backend.bat
echo.
echo Or manually:
echo   cd backend
echo   python -m uvicorn app.main:app --reload
echo.
pause
exit /b 0


@echo off
echo Setting up Frontend...
cd frontend

echo Installing Node.js dependencies...
call npm install

echo.
echo Frontend setup complete!
echo.
echo To start the frontend server, run:
echo   cd frontend
echo   npm run dev
echo.
pause



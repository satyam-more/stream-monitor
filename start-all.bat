@echo off
echo ========================================
echo Starting Stream Monitor System
echo ========================================
echo.
echo Starting Backend...
start "Backend Server" cmd /k "cd backend && venv\Scripts\activate && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
timeout /t 3 /nobreak >nul

echo Starting Frontend...
start "Frontend Server" cmd /k "cd frontend && npm run dev"
timeout /t 3 /nobreak >nul

echo Starting Simulator...
start "Simulator" cmd /k "cd simulator && ..\backend\venv\Scripts\python.exe simulator.py"

echo.
echo ========================================
echo All services started!
echo ========================================
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit (services will keep running)...
pause >nul

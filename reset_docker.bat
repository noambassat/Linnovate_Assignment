@echo off
echo ===== CHECKING DOCKER DESKTOP =====

REM Check if Docker Desktop is running
tasklist /FI "IMAGENAME eq Docker Desktop.exe" | find /I "Docker Desktop.exe" >nul
if errorlevel 1 (
    echo Starting Docker Desktop...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    timeout /t 20 >nul
) else (
    echo Docker Desktop is already running.
)

echo ===== WAITING FOR DOCKER ENGINE TO INITIALIZE =====
timeout /t 10

REM Clean all unused Docker resources
echo ===== PRUNING DOCKER SYSTEM =====
docker system prune -a -f

REM Change directory to the script location
cd /d "%~dp0"

REM Rebuild all images
echo ===== BUILDING DOCKER COMPOSE SERVICES =====
docker-compose build --no-cache

REM Start all services
echo ===== STARTING SERVICES =====
docker-compose up

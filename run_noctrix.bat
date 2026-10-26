@echo off
title NOCTRIX - Non-Human Identity Posture Management
cls
echo ======================================================================
echo                 NOCTRIX CONTROL CENTER & LAUNCHER
echo     Non-Human Identity Discovery, Graph Mapping & Remediation
echo ======================================================================
echo.
echo Please select an option:
echo.
echo   [1] Run Full Pipeline (Discovery -^> Graph -^> Risk -^> Remediation)
echo   [2] Launch Streamlit Visual Dashboard (Web UI)
echo   [3] Run Automated Test Suite (pytest)
echo   [4] Start Docker Containers (Neo4j ^& Vault)
echo   [5] Stop Docker Containers
echo   [6] Exit
echo.
echo ======================================================================
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" (
    cls
    echo [*] Running NOCTRIX Pipeline Orchestrator...
    python main.py
    echo.
    echo Press any key to return to menu...
    pause >nul
    "%~f0"
)

if "%choice%"=="2" (
    cls
    echo [*] Starting Streamlit Dashboard at http://localhost:8501...
    set PYTHONPATH=%APPDATA%\Python\Python312\site-packages
    streamlit run output/dashboard.py
    pause
    "%~f0"
)

if "%choice%"=="3" (
    cls
    echo [*] Running full test suite with pytest...
    pytest tests/ -v
    echo.
    echo Press any key to return to menu...
    pause >nul
    "%~f0"
)

if "%choice%"=="4" (
    cls
    echo [*] Starting Neo4j and Vault Docker containers...
    docker compose up -d
    echo.
    echo Neo4j Browser: http://localhost:7474 (neo4j / password)
    echo Vault Web UI:  http://localhost:8200 (token: root)
    echo.
    echo Press any key to return to menu...
    pause >nul
    "%~f0"
)

if "%choice%"=="5" (
    cls
    echo [*] Stopping Docker containers...
    docker compose down
    echo.
    echo Press any key to return to menu...
    pause >nul
    "%~f0"
)

if "%choice%"=="6" (
    exit /b
)

echo Invalid choice. Please try again.
pause
"%~f0"

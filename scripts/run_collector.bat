@echo off
REM GlobalProtect Debug Collector - Batch Wrapper
REM This script runs the Python collector with administrator privileges

echo ========================================
echo GlobalProtect Debug Collector
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Check if the main script exists
if not exist "globalprotect_debug_collector.py" (
    echo ERROR: globalprotect_debug_collector.py not found
    echo Please ensure you're running this from the correct directory
    pause
    exit /b 1
)

echo Python found. Starting collection...
echo.
echo Note: Some operations may require administrator privileges
echo.

REM Run the Python script
python globalprotect_debug_collector.py

echo.
echo Collection completed. Press any key to exit...
pause >nul

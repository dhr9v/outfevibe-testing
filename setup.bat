@echo off
REM Outfevibe Vision AI - Windows Setup Script

echo ========================================
echo Outfevibe Vision AI - Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo Checking Python version...
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist venv (
    echo WARNING: venv already exists. Removing old venv...
    rmdir /s /q venv
)
python -m venv venv
echo Virtual environment created
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1
echo pip upgraded
echo.

REM Install dependencies
echo Installing dependencies (this may take a few minutes)...
echo.

echo Installing Flask and core dependencies...
pip install Flask Flask-CORS python-dotenv werkzeug
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Flask dependencies
    pause
    exit /b 1
)

echo Installing image processing libraries...
pip install opencv-python Pillow numpy
if %errorlevel% neq 0 (
    echo ERROR: Failed to install image processing libraries
    pause
    exit /b 1
)

echo Installing MediaPipe...
pip install mediapipe
if %errorlevel% neq 0 (
    echo WARNING: MediaPipe installation failed. Trying alternative method...
    pip install mediapipe --no-cache-dir
    if %errorlevel% neq 0 (
        echo ERROR: MediaPipe installation failed. See TROUBLESHOOTING.md
        pause
        exit /b 1
    )
)

echo Installing ML libraries...
pip install scikit-learn
if %errorlevel% neq 0 (
    echo ERROR: Failed to install scikit-learn
    pause
    exit /b 1
)

echo Installing Google Gemini API...
pip install google-generativeai
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Gemini API
    pause
    exit /b 1
)

echo.
echo All dependencies installed successfully
echo.

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo .env file created
    echo.
    echo WARNING: Edit .env and add your GEMINI_API_KEY before running the app
    echo Get your API key: https://makersuite.google.com/app/apikey
    echo.
) else (
    echo .env file already exists
    echo.
)

REM Create uploads directory
if not exist uploads mkdir uploads
echo uploads\ directory ready
echo.

REM Run diagnostic
echo Running diagnostic check...
python diagnose.py
echo.

echo ========================================
echo Setup complete!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Add your Gemini API key to .env file
echo    (Open .env with notepad or your preferred editor)
echo.
echo 2. Activate virtual environment:
echo    venv\Scripts\activate
echo.
echo 3. Run the server:
echo    python app.py
echo.
echo 4. Test the API:
echo    python test_api.py path\to\your\image.jpg
echo.
echo Need help? Check TROUBLESHOOTING.md
echo.
pause

#!/bin/bash

# Outfevibe Vision AI - Quick Start Script

echo "🎨 Outfevibe Vision AI - Setup Script"
echo "======================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version detected"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  venv already exists. Removing old venv..."
    rm -rf venv
fi
python3 -m venv venv
echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✓ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies (this may take a few minutes)..."
echo "This will install: Flask, OpenCV, MediaPipe, Gemini API, and more..."
echo ""

# Install in stages to catch errors
echo "Installing Flask and core dependencies..."
pip install Flask Flask-CORS python-dotenv werkzeug || {
    echo "❌ Failed to install Flask dependencies"
    exit 1
}

echo "Installing image processing libraries..."
pip install opencv-python Pillow numpy || {
    echo "❌ Failed to install image processing libraries"
    exit 1
}

echo "Installing MediaPipe..."
pip install mediapipe || {
    echo "⚠️  MediaPipe installation failed. Trying alternative method..."
    pip install mediapipe --no-cache-dir || {
        echo "❌ MediaPipe installation failed. See TROUBLESHOOTING.md"
        exit 1
    }
}

echo "Installing ML libraries..."
pip install scikit-learn || {
    echo "❌ Failed to install scikit-learn"
    exit 1
}

echo "Installing Google Gemini API..."
pip install google-generativeai || {
    echo "❌ Failed to install Gemini API"
    exit 1
}

echo "✓ All dependencies installed successfully"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your GEMINI_API_KEY before running the app"
    echo "   Get your API key: https://makersuite.google.com/app/apikey"
    echo ""
else
    echo "✓ .env file already exists"
    echo ""
fi

# Create uploads directory
mkdir -p uploads
echo "✓ uploads/ directory ready"
echo ""

# Run diagnostic
echo "Running diagnostic check..."
python diagnose.py
echo ""

echo "✅ Setup complete!"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "Next steps:"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "1. Add your Gemini API key to .env file:"
echo "   nano .env  (or use your preferred editor)"
echo ""
echo "2. Activate virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "3. Run the server:"
echo "   python app.py"
echo ""
echo "4. Test the API:"
echo "   python test_api.py /path/to/your/image.jpg"
echo ""
echo "For Windows users:"
echo "  - Use: venv\\Scripts\\activate"
echo "  - Use: python instead of python3"
echo ""
echo "Need help? Check TROUBLESHOOTING.md"
echo ""

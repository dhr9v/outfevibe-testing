#!/bin/bash

# Installation script for Codespaces with MediaPipe fix

echo "============================================================"
echo "🎨 Outfevibe Vision AI - Codespaces Installation"
echo "============================================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version"
echo ""

# Upgrade pip first
echo "Upgrading pip, setuptools, and wheel..."
pip install --upgrade pip setuptools wheel
echo "✓ Done"
echo ""

# Install dependencies one by one to catch errors
echo "Installing dependencies..."
echo ""

echo "[1/9] Installing Flask..."
pip install Flask Flask-CORS || exit 1

echo "[2/9] Installing utilities..."
pip install python-dotenv werkzeug || exit 1

echo "[3/9] Installing Pillow..."
pip install Pillow || exit 1

echo "[4/9] Installing NumPy..."
pip install "numpy>=1.24.0,<2.0.0" || exit 1

echo "[5/9] Installing OpenCV (headless for Codespaces)..."
pip install opencv-python-headless || {
    echo "⚠️  Headless version failed, trying regular OpenCV..."
    pip install opencv-python || exit 1
}

echo "[6/9] Installing MediaPipe (finding compatible version)..."
pip install mediapipe || {
    echo "⚠️  Latest MediaPipe failed, trying specific versions..."
    pip install mediapipe==0.10.8 || \
    pip install mediapipe==0.10.7 || \
    pip install mediapipe==0.10.3 || {
        echo "❌ MediaPipe installation failed."
        echo "   This might be a platform compatibility issue."
        echo "   The app will still work but body/face detection may be limited."
    }
}

echo "[7/9] Installing scikit-learn..."
pip install scikit-learn || exit 1

echo "[8/9] Installing Google Gemini API..."
pip install google-generativeai || exit 1

echo "[9/9] Installing optional packages..."
pip install requests || true

echo ""
echo "✅ Installation complete!"
echo ""

# Create .env if doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ .env created"
    echo ""
    echo "⚠️  IMPORTANT: Add your GEMINI_API_KEY to .env"
    echo "   Get it from: https://makersuite.google.com/app/apikey"
    echo ""
fi

# Create uploads directory
mkdir -p uploads
mkdir -p static

echo "Running diagnostic..."
echo ""
python3 diagnose.py 2>/dev/null || {
    echo "⚠️  Diagnostic script not available yet"
}

echo ""
echo "============================================================"
echo "✅ Setup Complete!"
echo "============================================================"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your GEMINI_API_KEY"
echo "2. Run: python3 app.py"
echo "3. Open the PORTS tab and click the globe icon on port 5000"
echo ""
echo "For help: Check CODESPACES.md"
echo ""

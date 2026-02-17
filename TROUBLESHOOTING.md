# 🔧 Troubleshooting Guide

## Quick Diagnosis

Run the diagnostic script first:
```bash
python diagnose.py
```

This will tell you exactly what's wrong.

---

## Common Issues & Solutions

### Issue 1: "ModuleNotFoundError: No module named 'flask'"

**Problem**: Dependencies not installed

**Solution**:
```bash
# Make sure you're in the project directory
cd outfevibe-vision-ai

# Create virtual environment
python3 -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### Issue 2: "No module named 'sklearn'"

**Problem**: scikit-learn missing from requirements

**Solution**:
```bash
pip install scikit-learn
```

---

### Issue 3: "GEMINI_API_KEY not found"

**Problem**: Environment variables not configured

**Solution**:
```bash
# Copy example file
cp .env.example .env

# Edit .env file and add your key:
# GEMINI_API_KEY=your_actual_key_here
```

Get your API key: https://makersuite.google.com/app/apikey

---

### Issue 4: MediaPipe installation fails

**Problem**: Platform-specific MediaPipe issues

**Solutions**:

**For Apple Silicon (M1/M2/M3 Mac)**:
```bash
pip install mediapipe --no-cache-dir
```

**For Linux**:
```bash
sudo apt-get install -y python3-dev
pip install mediapipe
```

**For Windows**:
```bash
pip install mediapipe==0.10.9
```

**Alternative (if still failing)**:
```bash
# Try installing from wheel
pip install --upgrade pip setuptools wheel
pip install mediapipe
```

---

### Issue 5: OpenCV import error "ImportError: libGL.so.1"

**Problem**: Missing system libraries (Linux only)

**Solution**:
```bash
sudo apt-get update
sudo apt-get install -y libgl1-mesa-glx libglib2.0-0
```

Or use headless version:
```bash
pip uninstall opencv-python
pip install opencv-python-headless
```

---

### Issue 6: "Address already in use" / Port 5000 busy

**Problem**: Another process using port 5000

**Solution**:

**Option 1 - Change port**:
Edit `.env`:
```
PORT=8000
```

**Option 2 - Kill existing process**:
```bash
# Linux/Mac
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

---

### Issue 7: Image upload fails with "413 Payload Too Large"

**Problem**: Image file too large

**Solution**:
- Resize image before upload (max 10MB by default)
- Or increase limit in `.env`:
```
MAX_FILE_SIZE=20971520  # 20MB
```

---

### Issue 8: "No pose detected" or "No face detected"

**Problem**: Image quality or format issues

**Solution**:
- Use clear, well-lit full-body photo
- Ensure person is clearly visible and centered
- Use JPG or PNG format
- Try a different image

---

### Issue 9: Gemini API quota exceeded

**Problem**: Free tier API limits reached

**Solution**:
- Wait for quota reset (usually 24 hours)
- Check your quota: https://makersuite.google.com/app/apikey
- Consider upgrading API plan

---

### Issue 10: "Connection refused" when testing

**Problem**: Server not running

**Solution**:
```bash
# Make sure server is running in another terminal
python app.py

# Then test in a new terminal
python test_api.py /path/to/image.jpg
```

---

## Complete Fresh Install (Nuclear Option)

If nothing works, start completely fresh:

```bash
# 1. Delete old environment
rm -rf venv/

# 2. Create new virtual environment
python3 -m venv venv

# 3. Activate
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 4. Upgrade pip
pip install --upgrade pip

# 5. Install dependencies one by one
pip install Flask==3.0.0
pip install Flask-CORS==4.0.0
pip install opencv-python==4.8.1.78
pip install mediapipe==0.10.9
pip install Pillow==10.1.0
pip install numpy==1.24.3
pip install scikit-learn==1.3.2
pip install google-generativeai==0.3.2
pip install python-dotenv==1.0.0
pip install werkzeug==3.0.1

# 6. Configure .env
cp .env.example .env
# Edit .env and add GEMINI_API_KEY

# 7. Run diagnostic
python diagnose.py

# 8. Start server
python app.py
```

---

## Still Not Working?

**Step 1**: Run diagnostic script
```bash
python diagnose.py
```

**Step 2**: Check Python version
```bash
python --version  # Should be 3.8+
```

**Step 3**: Verify virtual environment
```bash
which python  # Should point to venv/bin/python
```

**Step 4**: Check the actual error message
```bash
python app.py  # Copy the full error message
```

**Step 5**: Enable debug mode
Edit `app.py` and change:
```python
if __name__ == '__main__':
    logger.info(f"Starting Outfevibe Vision AI on {Config.HOST}:{Config.PORT}")
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=True  # Enable debug mode
    )
```

---

## Testing Without Full Setup

If you just want to verify the code structure works, create a minimal test:

```python
# minimal_test.py
print("Testing imports...")

try:
    from flask import Flask
    print("✓ Flask")
except:
    print("✗ Flask - run: pip install Flask")

try:
    import cv2
    print("✓ OpenCV")
except:
    print("✗ OpenCV - run: pip install opencv-python")

try:
    import mediapipe
    print("✓ MediaPipe")
except:
    print("✗ MediaPipe - run: pip install mediapipe")

try:
    import google.generativeai as genai
    print("✓ Gemini")
except:
    print("✗ Gemini - run: pip install google-generativeai")

print("\nIf all show ✓, your setup is correct!")
```

Run it:
```bash
python minimal_test.py
```

---

## Getting Help

When asking for help, provide:
1. Output of `python diagnose.py`
2. Your Python version: `python --version`
3. Your OS (Windows/Mac/Linux)
4. Full error message
5. Output of `pip list`

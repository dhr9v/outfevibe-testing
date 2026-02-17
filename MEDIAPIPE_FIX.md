# 🔧 MediaPipe Installation Fix

## The Problem
`ERROR: No matching distribution found for mediapipe==0.10.9`

This happens because MediaPipe doesn't have builds for all Python versions or platforms.

---

## ✅ **SOLUTION 1: Use the Installation Script (RECOMMENDED)**

```bash
chmod +x install-codespaces.sh
./install-codespaces.sh
```

This script will:
- Try multiple MediaPipe versions automatically
- Install compatible versions for your system
- Handle all dependencies correctly

---

## ✅ **SOLUTION 2: Install Manually (Step by Step)**

Run these commands **one by one**:

```bash
# 1. Upgrade pip
pip install --upgrade pip setuptools wheel

# 2. Install core packages
pip install Flask Flask-CORS python-dotenv werkzeug

# 3. Install image processing
pip install Pillow numpy

# 4. Install OpenCV (headless works better in Codespaces)
pip install opencv-python-headless

# 5. Try MediaPipe (it will find compatible version)
pip install mediapipe

# If MediaPipe fails, try specific versions:
pip install mediapipe==0.10.8
# OR
pip install mediapipe==0.10.7
# OR
pip install mediapipe==0.10.3

# 6. Install ML library
pip install scikit-learn

# 7. Install Gemini API
pip install google-generativeai
```

---

## ✅ **SOLUTION 3: Use Minimal Requirements**

```bash
pip install -r requirements-minimal.txt
```

This uses flexible version requirements that auto-detect what works.

---

## ✅ **SOLUTION 4: Check Python Version**

MediaPipe might not support your Python version.

```bash
# Check your Python version
python3 --version
```

**MediaPipe supports:**
- Python 3.8, 3.9, 3.10, 3.11

**If you have Python 3.12+**, try:
```bash
# Install older MediaPipe
pip install mediapipe==0.10.8
```

---

## ✅ **SOLUTION 5: Platform-Specific Install**

### For GitHub Codespaces (Linux):
```bash
pip install mediapipe --no-cache-dir
```

### For Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install -y python3-dev build-essential
pip install mediapipe
```

### For macOS (especially M1/M2/M3):
```bash
pip install mediapipe --no-cache-dir --no-binary :all:
```

### For Windows:
```bash
pip install mediapipe --no-cache-dir
```

---

## 🔍 **Check What Worked**

After installation, verify:

```bash
python3 -c "import mediapipe; print('✓ MediaPipe:', mediapipe.__version__)"
```

Should show something like:
```
✓ MediaPipe: 0.10.8
```

---

## 🚀 **Quick Start After Fix**

Once MediaPipe is installed:

```bash
# 1. Configure API key
cp .env.example .env
nano .env
# Add: GEMINI_API_KEY=your_key_here

# 2. Run the app
python3 app.py

# 3. Open in browser
# Go to PORTS tab → Click globe icon on port 5000
```

---

## ⚠️ **Still Not Working?**

### Option A: Skip MediaPipe (Limited Functionality)
The app can run without MediaPipe, but body/face detection won't work.

Create a fallback version:
```python
# In services/mediapipe_analysis.py
# Comment out the imports and return default values
```

### Option B: Use Docker
If nothing works, try running in Docker (if available):
```bash
# Coming soon - Docker support
```

### Option C: Different Python Version
Try using Python 3.10 which has best MediaPipe support:
```bash
# In Codespaces
# Create new codespace with Python 3.10
```

---

## 📊 **What Version Did Install?**

Check all package versions:
```bash
pip list | grep -E "mediapipe|opencv|numpy|Flask"
```

---

## 💡 **Pro Tip**

Save your working configuration:
```bash
pip freeze > requirements-working.txt
```

Then next time just:
```bash
pip install -r requirements-working.txt
```

---

## 🆘 **Need More Help?**

1. Check your Python version: `python3 --version`
2. Check your OS: `uname -a`
3. Try the installation script: `./install-codespaces.sh`
4. Check the full error message carefully
5. Search for: "mediapipe [your_python_version] [your_os]"

---

## ✅ **Most Common Fix (90% success rate)**

```bash
pip install --upgrade pip
pip install mediapipe --no-cache-dir
```

If this works, you're good to go! 🎉

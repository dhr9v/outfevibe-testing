# 🚀 GitHub Codespaces Setup Guide

## Perfect! You're using GitHub Codespaces - here's how to get started:

### Step 1: Install Dependencies

**RECOMMENDED - Use the installation script:**
```bash
chmod +x install-codespaces.sh
./install-codespaces.sh
```

**OR install manually:**
```bash
# Upgrade pip first
pip install --upgrade pip setuptools wheel

# Try flexible requirements
pip install -r requirements.txt

# If MediaPipe fails, see MEDIAPIPE_FIX.md
```

**If you get MediaPipe errors**, run:
```bash
# This usually fixes it
pip install mediapipe --no-cache-dir
```

**Full troubleshooting**: See `MEDIAPIPE_FIX.md`

### Step 2: Configure API Key

```bash
# Create .env file
cp .env.example .env

# Edit .env file
nano .env
```

Add your Gemini API key:
```
GEMINI_API_KEY=your_actual_api_key_here
```

**Get your free API key**: https://makersuite.google.com/app/apikey

Press `Ctrl+X`, then `Y`, then `Enter` to save.

### Step 3: Run the Server

```bash
python app.py
```

You should see:
```
============================================================
🎨 Outfevibe Vision AI - Starting Server
============================================================
Server running on: http://0.0.0.0:5000
Web Interface: http://localhost:5000
Health Check: http://localhost:5000/health
============================================================
```

### Step 4: Access the Web Interface

**In GitHub Codespaces:**

1. Look for a popup notification that says: "Your application running on port 5000 is available"
2. Click **"Open in Browser"** or **"Preview in Editor"**

**OR manually:**

1. Go to the **PORTS** tab (next to TERMINAL)
2. Find port **5000**
3. Click the **globe icon** 🌐 to open in browser

### Step 5: Test It!

Once the web interface opens:

1. **Upload a full-body image** (drag & drop or click to browse)
2. *Optional:* Click "Add Personalization" to specify mood, occasion, etc.
3. Click **"Analyze Image"**
4. Wait 10-15 seconds for AI analysis
5. View your personalized recommendations!

---

## 🎯 Using the API Directly

### Health Check
```bash
curl http://localhost:5000/health
```

### Analyze Image
```bash
curl -X POST http://localhost:5000/analyze \
  -F "image=@/path/to/image.jpg"
```

### With Personalization
```bash
curl -X POST http://localhost:5000/personalize \
  -F "image=@/path/to/image.jpg" \
  -F "mood=confident" \
  -F "occasion=business_meeting"
```

---

## 🔧 Troubleshooting in Codespaces

### "Address already in use"
```bash
# Kill existing process
pkill -f "python app.py"

# Or use a different port
# Edit .env: PORT=8000
```

### Can't access the web interface?
1. Check PORTS tab in VS Code
2. Make sure port 5000 is listed
3. Visibility should be "Public" or "Private"
4. Click the globe icon to open

### Still getting "Endpoint not found"?
- Make sure you're accessing the **root URL** (`http://localhost:5000/`)
- NOT `/analyze` directly in browser
- The web interface will handle API calls for you

### Need to reinstall?
```bash
pip install --upgrade --force-reinstall -r requirements.txt
```

---

## 📊 Quick Diagnostic

```bash
# Run diagnostic script
python diagnose.py
```

This will check:
- ✓ Python version
- ✓ All required packages
- ✓ .env configuration
- ✓ Directory structure

---

## 🎨 What You Can Do

### Basic Analysis
- Upload full-body image
- Get body shape analysis
- Get face shape analysis
- Get skin tone & undertone
- Receive AI outfit recommendations

### Personalized Analysis
- Add mood (confident, relaxed, etc.)
- Specify occasion (business, date, party, etc.)
- Include weather conditions
- Set budget preferences
- Get tailored recommendations

---

## 🌐 Making it Public

To share your Codespace app:

1. Go to **PORTS** tab
2. Right-click on port **5000**
3. Select **"Port Visibility" → "Public"**
4. Copy the forwarded URL
5. Share with anyone!

---

## 💡 Pro Tips for Codespaces

### Keep Codespace Alive
Codespaces auto-suspend after inactivity. To prevent this:
- Keep the browser tab open
- Ping the health endpoint periodically

### Upload Test Images
You can upload images directly to Codespaces:
1. Right-click in Explorer panel
2. Select "Upload..."
3. Choose your image file

### View Logs
```bash
# See detailed logs while running
python app.py
```

All requests and responses will be logged in real-time.

---

## ❓ Common Questions

**Q: Why do I see "Method not allowed" when I visit /analyze?**  
A: `/analyze` is a POST endpoint. Use the web interface at the root URL `/` instead, or send POST requests via curl/Python.

**Q: Can I use this API in my frontend app?**  
A: Yes! The API supports CORS. Just make POST requests to the endpoints.

**Q: How do I stop the server?**  
A: Press `Ctrl+C` in the terminal where it's running.

**Q: Where are uploaded images stored?**  
A: Temporarily in the `uploads/` folder. They're deleted immediately after processing.

---

## 🎉 You're All Set!

Your Fashion AI is ready to use! Open the web interface and start analyzing images.

For more details, check:
- `README.md` - Full documentation
- `TROUBLESHOOTING.md` - Common issues
- `QUICKSTART.md` - Quick reference

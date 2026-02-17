# ⚡ QUICK START GUIDE

## Prerequisites
- **Python 3.8+** installed
- **Internet connection** for downloading packages
- **Google Gemini API Key** ([Get it free here](https://makersuite.google.com/app/apikey))

---

## 🚀 Setup in 3 Minutes

### For Linux/Mac Users:

```bash
# 1. Run setup script
chmod +x setup.sh
./setup.sh

# 2. Edit .env and add your API key
nano .env
# Add: GEMINI_API_KEY=your_key_here

# 3. Start the server
source venv/bin/activate
python app.py
```

### For Windows Users:

```cmd
# 1. Run setup script
setup.bat

# 2. Edit .env and add your API key
notepad .env
REM Add: GEMINI_API_KEY=your_key_here

# 3. Start the server
venv\Scripts\activate
python app.py
```

---

## ✅ Verify It's Working

### Test 1: Health Check
Open browser: http://localhost:5000/health

Should see:
```json
{
  "status": "healthy",
  "service": "Outfevibe Vision AI",
  "version": "1.0.0"
}
```

### Test 2: API Test
```bash
# With a full-body image
python test_api.py path/to/image.jpg
```

---

## 📤 Make Your First Request

### Using cURL:
```bash
curl -X POST http://localhost:5000/analyze \
  -F "image=@/path/to/image.jpg"
```

### Using Python:
```python
import requests

url = "http://localhost:5000/analyze"
files = {'image': open('image.jpg', 'rb')}
response = requests.post(url, files=files)
print(response.json())
```

### Using Postman:
1. Create new POST request
2. URL: `http://localhost:5000/analyze`
3. Body → form-data
4. Key: `image` (type: File)
5. Select your image
6. Send!

---

## 🎯 Expected Response

```json
{
  "analysis": {
    "body_shape": "inverted_triangle",
    "face_shape": "oval",
    "skin_tone": "medium",
    "undertone": "warm",
    "dominant_colors": ["#3b5998", "#8b4513", "#ffffff"]
  },
  "recommendations": {
    "recommended_categories": [
      "A-line dresses",
      "Wide-leg pants",
      "V-neck tops"
    ],
    "recommended_colors": [
      {"name": "coral", "hex": "#FF7F50"},
      {"name": "olive_green", "hex": "#808000"}
    ],
    "styling_tips": [
      "Balance your shoulders with A-line silhouettes",
      "Embrace warm earth tones"
    ]
  },
  "status": "success"
}
```

---

## 🔧 Common Issues

### "ModuleNotFoundError"
```bash
# Activate venv first!
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Then install
pip install -r requirements.txt
```

### "GEMINI_API_KEY not found"
```bash
# Make sure .env exists
cp .env.example .env

# Add your key
echo "GEMINI_API_KEY=your_key_here" >> .env
```

### Port 5000 busy
```bash
# Change port in .env
echo "PORT=8000" >> .env
```

### More issues?
Check `TROUBLESHOOTING.md` or run:
```bash
python diagnose.py
```

---

## 📱 Next Steps

1. **Integrate with Frontend**
   - Build React/Vue.js UI
   - Add file upload component
   - Display recommendations

2. **Deploy to Cloud**
   - Use Gunicorn for production
   - Deploy to Heroku/Railway/Render
   - Add cloud storage (AWS S3)

3. **Enhance Features**
   - Add user authentication
   - Save analysis history
   - Product recommendations
   - Style boards

---

## 🆘 Need Help?

1. Run diagnostic: `python diagnose.py`
2. Check: `TROUBLESHOOTING.md`
3. Review: `README.md`

---

**You're all set! Happy coding! 🎉**

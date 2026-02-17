# 🎨 Outfevibe Vision AI - Backend MVP

AI-powered fashion recommendation system that analyzes body shape, face shape, and skin tone to provide personalized styling advice.

## 📋 Features

- **Body Shape Analysis**: Detects body proportions using MediaPipe pose detection
- **Face Shape Analysis**: Identifies face shape through facial landmark detection
- **Color Analysis**: Extracts skin tone, undertone, and dominant clothing colors
- **AI Recommendations**: Generates personalized outfit suggestions using Google Gemini
- **Personalization**: Optional context-aware recommendations based on mood, occasion, weather, and budget

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Image Processing**: OpenCV
- **Body/Face Detection**: MediaPipe
- **AI Engine**: Google Gemini API
- **Color Analysis**: K-means clustering
- **Storage**: Local file system (easily extensible to cloud)

## 📁 Project Structure

```
outfevibe-vision-ai/
├── app.py                          # Main Flask application
├── config.py                       # Configuration settings
├── requirements.txt                # Dependencies
├── .env.example                    # Environment template
├── services/
│   ├── image_processing.py         # Image preprocessing
│   ├── mediapipe_analysis.py       # Body & face detection
│   ├── color_analysis.py           # Skin tone & color extraction
│   └── gemini_service.py           # AI recommendations
├── utils/
│   ├── logger.py                   # Logging setup
│   └── validators.py               # File validation
└── uploads/                        # Temporary image storage
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Google Gemini API key ([Get it here](https://makersuite.google.com/app/apikey))

### Step 1: Clone & Navigate

```bash
cd outfevibe-vision-ai
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your API key
# GEMINI_API_KEY=your_actual_api_key_here
```

### Step 5: Run the Server

```bash
python app.py
```

Server will start on `http://localhost:5000`

## 📡 API Endpoints

### 1. Health Check

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "service": "Outfevibe Vision AI",
  "version": "1.0.0"
}
```

### 2. Analyze Fashion (Main Endpoint)

**Endpoint**: `POST /analyze`

**Request**: Multipart form-data
- `image`: Image file (jpg, jpeg, png)

**Response**:
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
      "V-neck tops",
      "Wrap dresses"
    ],
    "recommended_colors": [
      {"name": "coral", "hex": "#FF7F50"},
      {"name": "olive_green", "hex": "#808000"},
      {"name": "warm_beige", "hex": "#D4A574"}
    ],
    "styling_tips": [
      "Balance your shoulders with A-line silhouettes",
      "Embrace warm earth tones that complement your undertone",
      "Try statement necklaces to draw attention to your face"
    ]
  },
  "status": "success"
}
```

### 3. Personalized Recommendations (Bonus)

**Endpoint**: `POST /personalize`

**Request**: Multipart form-data
- `image`: Image file
- `mood`: (optional) e.g., "confident", "relaxed"
- `occasion`: (optional) e.g., "business meeting", "date night"
- `weather`: (optional) e.g., "sunny", "cold"
- `budget`: (optional) e.g., "affordable", "luxury"

**Response**: Same structure as `/analyze` but with personalized context

## 🧪 Testing with cURL

### Basic Analysis

```bash
curl -X POST http://localhost:5000/analyze \
  -F "image=@/path/to/your/image.jpg"
```

### Personalized Analysis

```bash
curl -X POST http://localhost:5000/personalize \
  -F "image=@/path/to/your/image.jpg" \
  -F "mood=confident" \
  -F "occasion=business meeting" \
  -F "weather=cold" \
  -F "budget=mid-range"
```

## 🧪 Testing with Python

```python
import requests

# Basic analysis
url = "http://localhost:5000/analyze"
files = {'image': open('test_image.jpg', 'rb')}
response = requests.post(url, files=files)
print(response.json())

# Personalized analysis
url = "http://localhost:5000/personalize"
files = {'image': open('test_image.jpg', 'rb')}
data = {
    'mood': 'confident',
    'occasion': 'date night',
    'weather': 'warm',
    'budget': 'mid-range'
}
response = requests.post(url, files=files, data=data)
print(response.json())
```

## 🔧 Configuration

Edit `config.py` or `.env` to customize:

- `MAX_FILE_SIZE`: Maximum upload size (default: 10MB)
- `IMAGE_MAX_WIDTH`: Max image width for processing (default: 800px)
- `IMAGE_MAX_HEIGHT`: Max image height for processing (default: 1200px)
- `ALLOWED_EXTENSIONS`: Supported file types

## 🐛 Troubleshooting

### MediaPipe Installation Issues

If you encounter MediaPipe installation errors:

```bash
# Install with specific version
pip install mediapipe==0.10.9 --no-cache-dir

# Or try pre-built wheel
pip install --upgrade pip setuptools wheel
pip install mediapipe
```

### OpenCV Import Errors

```bash
# Reinstall OpenCV
pip uninstall opencv-python
pip install opencv-python-headless
```

### Gemini API Errors

- Verify API key is correct in `.env`
- Check API quota limits
- Ensure internet connection is stable

## 📊 Performance Optimization

- Images are automatically resized to max 800x1200px
- Temporary files are cleaned up after processing
- K-means clustering uses optimized parameters
- MediaPipe runs in static image mode for efficiency

## 🔒 Security Notes

- File type validation prevents malicious uploads
- File size limits prevent DoS attacks
- Temporary files are immediately deleted after processing
- Consider adding rate limiting for production

## 🚀 Production Deployment

### Recommended Additions:

1. **Cloud Storage**: Replace local uploads with AWS S3/Google Cloud Storage
2. **Database**: Add Supabase integration for user history
3. **Rate Limiting**: Use Flask-Limiter
4. **Authentication**: Add JWT authentication
5. **HTTPS**: Deploy behind reverse proxy (nginx)
6. **Monitoring**: Add error tracking (Sentry)

### Deploy with Gunicorn

```bash
pip install gunicorn

gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📝 Next Steps

- [ ] Add user authentication
- [ ] Store analysis history in database
- [ ] Implement caching for repeated analyses
- [ ] Add fashion product recommendations
- [ ] Create frontend interface
- [ ] Deploy to cloud platform

## 🤝 Contributing

This is an MVP. For production use:
- Add comprehensive unit tests
- Implement CI/CD pipeline
- Add API documentation (Swagger)
- Enhance error handling
- Add request validation middleware

## 📄 License

MIT License - Feel free to use for your projects!

## 🙏 Acknowledgments

- MediaPipe by Google
- Google Gemini API
- OpenCV community
- Flask framework

---

**Version**: 1.0.0 MVP  
**Status**: Development  
**Last Updated**: 2026
# outfevibe-testing

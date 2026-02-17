"""
Debug script to test each component individually
"""
import os
import sys
from config import Config
from utils import setup_logger
from services import ImageProcessor, MediaPipeAnalyzer, ColorAnalyzer, GeminiService

# Setup
logger = setup_logger(__name__)

def test_gemini_api():
    """Test if Gemini API is working"""
    print("Testing Gemini API connection...")
    try:
        gemini_service = GeminiService()
        print("✓ Gemini service initialized")
        
        # Test with sample data
        sample_data = {
            'body_shape': 'rectangle',
            'face_shape': 'oval',
            'skin_tone': 'medium',
            'undertone': 'warm',
            'dominant_colors': ['#3b5998', '#8b4513']
        }
        
        print("Sending test request to Gemini...")
        response = gemini_service.generate_recommendations(sample_data)
        print("✓ Gemini API working correctly")
        print(f"Sample response: {response}")
        return True
    except Exception as e:
        print(f"✗ Gemini API error: {str(e)}")
        return False

def test_mediapipe():
    """Test MediaPipe functionality"""
    print("\nTesting MediaPipe...")
    try:
        analyzer = MediaPipeAnalyzer()
        print("✓ MediaPipe analyzer initialized")
        return True
    except Exception as e:
        print(f"✗ MediaPipe error: {str(e)}")
        return False

def test_color_analysis():
    """Test color analysis"""
    print("\nTesting Color Analysis...")
    try:
        analyzer = ColorAnalyzer()
        print("✓ Color analyzer initialized")
        return True
    except Exception as e:
        print(f"✗ Color analysis error: {str(e)}")
        return False

def test_image_processing():
    """Test image processing"""
    print("\nTesting Image Processing...")
    try:
        processor = ImageProcessor()
        print("✓ Image processor initialized")
        return True
    except Exception as e:
        print(f"✗ Image processing error: {str(e)}")
        return False

def main():
    print("=" * 50)
    print("Outfevibe Vision AI - Component Debug Test")
    print("=" * 50)
    
    results = []
    results.append(test_image_processing())
    results.append(test_mediapipe())
    results.append(test_color_analysis())
    results.append(test_gemini_api())
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✅ All components working!")
    else:
        print("❌ Some components failed")
        print("\nNext steps:")
        if not results[3]:  # Gemini failed
            print("1. Get a new Gemini API key from https://makersuite.google.com/app/apikey")
            print("2. Update your .env file with the new key")
        print("3. Restart the server: python app.py")

if __name__ == "__main__":
    main()
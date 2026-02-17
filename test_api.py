"""
Test script for Outfevibe Vision AI API
Run this after starting the server to verify endpoints
"""

import requests
import json
import sys

BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test health check endpoint"""
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✓ Health check passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"✗ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Health check error: {str(e)}")
        return False

def test_analyze_endpoint(image_path=None):
    """Test analyze endpoint"""
    print("\n2. Testing Analyze Endpoint...")
    
    if not image_path:
        print("⚠ No image provided. Skipping analyze test.")
        print("  Usage: python test_api.py /path/to/image.jpg")
        return False
    
    try:
        with open(image_path, 'rb') as img:
            files = {'image': img}
            response = requests.post(f"{BASE_URL}/analyze", files=files)
        
        if response.status_code == 200:
            print("✓ Analyze endpoint working")
            result = response.json()
            print(f"\n   Analysis Results:")
            print(f"   - Body Shape: {result['analysis']['body_shape']}")
            print(f"   - Face Shape: {result['analysis']['face_shape']}")
            print(f"   - Skin Tone: {result['analysis']['skin_tone']}")
            print(f"   - Undertone: {result['analysis']['undertone']}")
            print(f"\n   Recommendations:")
            print(f"   - Categories: {', '.join(result['recommendations']['recommended_categories'][:3])}")
            print(f"   - Colors: {len(result['recommendations']['recommended_colors'])} suggested")
            return True
        else:
            print(f"✗ Analyze failed: {response.status_code}")
            print(f"   Error: {response.json()}")
            return False
    
    except FileNotFoundError:
        print(f"✗ Image file not found: {image_path}")
        return False
    except Exception as e:
        print(f"✗ Analyze error: {str(e)}")
        return False

def test_personalize_endpoint(image_path=None):
    """Test personalize endpoint"""
    print("\n3. Testing Personalize Endpoint...")
    
    if not image_path:
        print("⚠ No image provided. Skipping personalize test.")
        return False
    
    try:
        with open(image_path, 'rb') as img:
            files = {'image': img}
            data = {
                'mood': 'confident',
                'occasion': 'business meeting',
                'weather': 'cold',
                'budget': 'mid-range'
            }
            response = requests.post(f"{BASE_URL}/personalize", files=files, data=data)
        
        if response.status_code == 200:
            print("✓ Personalize endpoint working")
            result = response.json()
            print(f"\n   Personalization: {result['personalization']}")
            print(f"   Recommendations tailored for: {result['personalization'].get('occasion', 'N/A')}")
            return True
        else:
            print(f"✗ Personalize failed: {response.status_code}")
            print(f"   Error: {response.json()}")
            return False
    
    except Exception as e:
        print(f"✗ Personalize error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("Outfevibe Vision AI - API Test Suite")
    print("=" * 50)
    
    # Get image path from command line
    image_path = sys.argv[1] if len(sys.argv) > 1 else None
    
    # Run tests
    results = []
    results.append(test_health_check())
    results.append(test_analyze_endpoint(image_path))
    results.append(test_personalize_endpoint(image_path))
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✅ All tests passed!")
    else:
        print("⚠️  Some tests failed or were skipped")
        if not image_path:
            print("\nTip: Provide an image path to run full tests:")
            print("python test_api.py /path/to/image.jpg")

if __name__ == "__main__":
    main()

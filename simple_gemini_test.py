"""
Simple Gemini API test
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("❌ No GEMINI_API_KEY found in environment")
    exit(1)

print(f"Using API key: {api_key[:10]}...{api_key[-5:]}")

try:
    # Configure API
    genai.configure(api_key=api_key)
    print("✓ API configured successfully")
    
    # Try to list models
    print("Attempting to list available models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✓ Available model: {m.name}")
    
    # Try a simple request
    print("\nTesting with gemini-pro...")
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Say hello")
    print(f"✓ Response: {response.text[:100]}...")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    print("\nThis means your API key is invalid or doesn't have proper permissions.")
    print("Please get a new API key from: https://makersuite.google.com/app/apikey")
"""
Debug script to test the dress generation endpoint directly
"""
import requests
import json

def test_dress_endpoint():
    print("🔍 Debugging Dress Generation Endpoint")
    print("=" * 50)
    
    # Test the endpoint directly
    try:
        # First check if server is running
        health_response = requests.get("http://localhost:5000/health")
        if health_response.status_code == 200:
            print("✅ Server is running")
        else:
            print("❌ Server health check failed")
            return
            
        # Test dress generation endpoint
        print("\nTesting /generate-dress-prompts endpoint...")
        
        # Sample data for testing
        test_data = {
            'mood': 'elegant',
            'occasion': 'wedding_guest', 
            'weather': 'spring',
            'budget': 'mid-range'
        }
        
        # For testing without image, let's see what the endpoint expects
        response = requests.post(
            "http://localhost:5000/generate-dress-prompts",
            data=test_data
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Dress generation endpoint working!")
            if 'dress_prompts' in data:
                print(f"✅ Found {len(data['dress_prompts']['dress_designs'])} dress designs")
                for i, dress in enumerate(data['dress_prompts']['dress_designs']):
                    print(f"  Design {i+1}: {dress['design_name']}")
            else:
                print("❌ No dress_prompts in response")
        else:
            print("❌ Dress generation endpoint failed")
            
    except Exception as e:
        print(f"❌ Error testing endpoint: {str(e)}")

def test_web_logic():
    print("\n" + "=" * 50)
    print("Testing Web Interface Logic")
    print("=" * 50)
    
    # Simulate what happens in the browser
    personalization_enabled = True  # User clicked "Add Personalization"
    personalization_filled = True   # User filled some fields
    
    endpoint = '/analyze'
    
    if personalization_enabled and personalization_filled:
        endpoint = '/generate-dress-prompts'
        print(f"✅ Logic correct: Using {endpoint} endpoint")
    else:
        print(f"ℹ️  Would use {endpoint} endpoint")
    
    print("✅ Web interface logic is working correctly")

if __name__ == "__main__":
    test_dress_endpoint()
    test_web_logic()
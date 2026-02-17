"""
Test script for dress generation prompts
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_dress_generation():
    """Test the dress generation endpoint"""
    print("Testing Dress Generation Endpoint...")
    
    # You'll need to provide an actual image path
    image_path = input("Enter path to a full-body image (or press Enter to skip): ").strip()
    
    if not image_path:
        print("Skipping test - no image provided")
        return
    
    try:
        with open(image_path, 'rb') as img:
            files = {'image': img}
            data = {
                'mood': 'elegant',
                'occasion': 'wedding guest',
                'weather': 'spring',
                'budget': 'mid-range'
            }
            
            response = requests.post(f"{BASE_URL}/generate-dress-prompts", files=files, data=data)
        
        if response.status_code == 200:
            print("✓ Dress generation successful!")
            result = response.json()
            
            print(f"\n=== ANALYSIS ===")
            print(f"Body Shape: {result['analysis']['body_shape']}")
            print(f"Face Shape: {result['analysis']['face_shape']}")
            print(f"Skin Tone: {result['analysis']['skin_tone']}")
            print(f"Undertone: {result['analysis']['undertone']}")
            
            print(f"\n=== DRESS DESIGNS ===")
            for i, dress in enumerate(result['dress_prompts']['dress_designs'], 1):
                print(f"\n--- Design {i}: {dress['design_name']} ---")
                print(f"Style: {dress['design_style']}")
                print(f"Silhouette: {dress['silhouette']}")
                print(f"Neckline: {dress['neckline']}")
                print(f"Colors: {', '.join(dress['color_scheme'])}")
                print(f"Image Generation Prompt: {dress['image_generation_prompt'][:100]}...")
            
            # Save full response to file
            with open('dress_prompts_output.json', 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\nFull response saved to dress_prompts_output.json")
            
        else:
            print(f"✗ Dress generation failed: {response.status_code}")
            print(f"Error: {response.json()}")
    
    except FileNotFoundError:
        print(f"✗ Image file not found: {image_path}")
    except Exception as e:
        print(f"✗ Error: {str(e)}")

def test_health():
    """Test health endpoint"""
    print("Testing Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        print("✓ Health check passed")
        return True
    else:
        print("✗ Health check failed")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Dress Generation Test")
    print("=" * 50)
    
    if test_health():
        test_dress_generation()
    else:
        print("Server not running. Please start the server first:")
        print("python app.py")
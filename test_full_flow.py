"""
Create a simple test image and demonstrate the full flow
"""
import requests
import json
from PIL import Image, ImageDraw
import io
import base64

def create_test_image():
    """Create a simple test image"""
    # Create a simple colored rectangle image
    img = Image.new('RGB', (400, 600), color=(128, 128, 128))
    draw = ImageDraw.Draw(img)
    
    # Add some basic shapes to make it look like a person outline
    # Body rectangle
    draw.rectangle([150, 100, 250, 400], fill=(200, 150, 150))
    # Head circle
    draw.ellipse([175, 50, 225, 100], fill=(200, 150, 150))
    # Arms
    draw.rectangle([120, 150, 150, 250], fill=(200, 150, 150))
    draw.rectangle([250, 150, 280, 250], fill=(200, 150, 150))
    
    # Save to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    return img_bytes

def test_full_flow():
    """Test the complete flow with image upload"""
    print("🧪 Testing Complete Flow with Image Upload")
    print("=" * 50)
    
    try:
        # Create test image
        print("Creating test image...")
        test_image = create_test_image()
        
        # Prepare form data
        files = {'image': ('test_image.jpg', test_image, 'image/jpeg')}
        data = {
            'mood': 'elegant',
            'occasion': 'wedding_guest',
            'weather': 'spring',
            'budget': 'mid-range'
        }
        
        print("Sending request to /generate-dress-prompts...")
        response = requests.post(
            "http://localhost:5000/generate-dress-prompts",
            files=files,
            data=data
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success! Dress prompts generated")
            
            print(f"\nAnalysis Results:")
            print(f"- Body Shape: {result['analysis']['body_shape']}")
            print(f"- Face Shape: {result['analysis']['face_shape']}")
            print(f"- Skin Tone: {result['analysis']['skin_tone']}")
            print(f"- Undertone: {result['analysis']['undertone']}")
            
            print(f"\nPersonalization: {result['personalization']}")
            
            print(f"\nDress Designs Generated: {len(result['dress_prompts']['dress_designs'])}")
            for i, dress in enumerate(result['dress_prompts']['dress_designs'], 1):
                print(f"\n--- Design {i}: {dress['design_name']} ---")
                print(f"Style: {dress['design_style']}")
                print(f"Colors: {', '.join(dress['color_scheme'])}")
                print(f"Prompt length: {len(dress['image_generation_prompt'])} characters")
            
            # Save result for inspection
            with open('full_flow_test_result.json', 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\n✅ Full result saved to full_flow_test_result.json")
            
            return True
        else:
            print(f"❌ Request failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def show_instructions():
    """Show instructions for using the web interface"""
    print("\n" + "=" * 50)
    print("📋 How to Use the Web Interface")
    print("=" * 50)
    print("1. Click the preview button to open the web interface")
    print("2. Click in the upload area or drag/drop an image")
    print("3. Click 'Add Personalization (Optional)'")
    print("4. Fill in at least one personalization field:")
    print("   - Mood (elegant, casual, etc.)")
    print("   - Occasion (wedding, business, etc.)")
    print("   - Weather (sunny, cold, etc.)")
    print("   - Budget (affordable, mid-range, etc.)")
    print("5. Click 'Analyze Image'")
    print("6. Scroll down to see the dress generation prompts!")
    print("\n✨ The 3 dress designs will appear with:")
    print("   - Copy buttons for each prompt")
    print("   - Design details")
    print("   - AI tool integration buttons")

if __name__ == "__main__":
    success = test_full_flow()
    
    if success:
        print("\n🎉 The system is working correctly!")
        print("The dress prompts should now appear in the web interface.")
    else:
        print("\n❌ There was an issue with the test.")
    
    show_instructions()
"""
Quick test for dress generation using sample analysis data
"""
import sys
import os
sys.path.append('.')

from services.gemini_service import GeminiService
from config import Config

def test_dress_generation_with_sample_data():
    """Test dress generation with sample analysis data"""
    
    # Sample analysis data (what would come from image analysis)
    sample_analysis = {
        'body_shape': 'rectangle',
        'face_shape': 'oval', 
        'skin_tone': 'medium',
        'undertone': 'warm',
        'dominant_colors': ['#3b5998', '#8b4513', '#ffffff']
    }
    
    # Sample personalization
    personalization = {
        'mood': 'elegant',
        'occasion': 'wedding_guest',
        'weather': 'spring',
        'budget': 'mid-range'
    }
    
    print("Testing Dress Generation with Sample Data...")
    print("=" * 50)
    
    try:
        # Initialize Gemini service
        gemini_service = GeminiService()
        print("✓ Gemini service initialized")
        
        # Generate dress prompts
        print("\nGenerating dress design prompts...")
        dress_prompts = gemini_service.generate_dress_prompts(
            sample_analysis, 
            personalization
        )
        
        print("✓ Dress prompts generated successfully!")
        
        # Display results
        print("\n" + "=" * 50)
        print("DRESS DESIGNS GENERATED:")
        print("=" * 50)
        
        for i, dress in enumerate(dress_prompts['dress_designs'], 1):
            print(f"\n--- DESIGN {i}: {dress['design_name']} ---")
            print(f"Style: {dress['design_style']}")
            print(f"Silhouette: {dress['silhouette']}")
            print(f"Neckline: {dress['neckline']}")
            print(f"Colors: {', '.join(dress['color_scheme'])}")
            print(f"Length: {dress['length']}")
            print(f"Accessories: {', '.join(dress['accessories'])}")
            print(f"\n🎯 IMAGE GENERATION PROMPT:")
            print(f"{dress['image_generation_prompt']}")
            print("-" * 50)
        
        # Save to file
        import json
        with open('sample_dress_prompts.json', 'w') as f:
            json.dump(dress_prompts, f, indent=2)
        print(f"\n✅ Full response saved to sample_dress_prompts.json")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    # Test the function
    success = test_dress_generation_with_sample_data()
    
    if success:
        print("\n🎉 Dress generation is working correctly!")
        print("You can now use the /generate-dress-prompts endpoint with real images.")
    else:
        print("\n❌ There was an error with dress generation.")
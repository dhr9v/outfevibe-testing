# 🎨 Dress Generation API

## New Endpoint: `/generate-dress-prompts`

Generate detailed dress design prompts optimized for image generation AI based on personal analysis.

### Request
**Method**: `POST`  
**Content-Type**: `multipart/form-data`

**Required Fields:**
- `image`: Full-body photo file (jpg, jpeg, png)

**Optional Fields:**
- `mood`: Style preference (e.g., "elegant", "casual", "bohemian")
- `occasion`: Event type (e.g., "wedding", "business", "date night")
- `weather`: Climate conditions (e.g., "summer", "winter", "spring")
- `budget`: Price range (e.g., "affordable", "luxury", "mid-range")

### Response Format

```json
{
  "analysis": {
    "body_shape": "rectangle",
    "face_shape": "oval",
    "skin_tone": "medium",
    "undertone": "warm",
    "dominant_colors": ["#3b5998", "#8b4513"]
  },
  "personalization": {
    "mood": "elegant",
    "occasion": "wedding guest",
    "weather": "spring"
  },
  "dress_prompts": {
    "dress_designs": [
      {
        "design_name": "Elegant A-line Cocktail Dress",
        "design_style": "Classic sophisticated silhouette",
        "silhouette": "A-line shape that creates curves for rectangular body type",
        "neckline": "Sweetheart neckline that complements oval face shape",
        "sleeves": "Cap sleeves for balanced proportions",
        "fabric": "Lightweight crepe or silk blend",
        "color_scheme": ["warm beige", "terracotta", "deep teal"],
        "pattern_details": "Minimal clean lines with subtle waist definition",
        "length": "Knee-length for professional occasions",
        "fit": "Fitted bodice with flowing skirt",
        "accessories": ["pearl earrings", "delicate necklace"],
        "image_generation_prompt": "Professional fashion photography of an elegant A-line dress with sweetheart neckline, cap sleeves, in warm beige color, lightweight fabric with subtle drape, photographed on a professional model with studio lighting, high fashion editorial style"
      }
    ]
  },
  "status": "success"
}
```

### Example Usage

#### cURL
```bash
curl -X POST http://localhost:5000/generate-dress-prompts \
  -F "image=@/path/to/your/image.jpg" \
  -F "mood=elegant" \
  -F "occasion=wedding_guest" \
  -F "weather=spring"
```

#### Python
```python
import requests

url = "http://localhost:5000/generate-dress-prompts"
files = {'image': open('image.jpg', 'rb')}
data = {
    'mood': 'elegant',
    'occasion': 'wedding_guest',
    'weather': 'spring'
}

response = requests.post(url, files=files, data=data)
result = response.json()

# Extract image generation prompts
for dress in result['dress_prompts']['dress_designs']:
    print(dress['image_generation_prompt'])
```

### Using with Image Generation AI

The `image_generation_prompt` field contains detailed descriptions ready for:
- **DALL-E**: Copy the prompt directly
- **Midjourney**: Use as your prompt input
- **Stable Diffusion**: Perfect for txt2img generation
- **Other AI art tools**: Works with any text-to-image system

### Key Features

✅ **Personalized Design**: Each prompt considers body shape, face shape, and skin tone  
✅ **Context-Aware**: Adapts to mood, occasion, weather, and budget  
✅ **Professional Quality**: Detailed enough for commercial fashion photography  
✅ **Multiple Options**: Generates 3 different dress designs per request  
✅ **Ready-to-Use**: No additional formatting needed for image generation tools

### Sample Image Generation Prompts

The system generates prompts like:
> "Professional fashion photography of a flowing bohemian maxi dress with deep V-neckline, three-quarter sleeves, in rich terracotta and olive green color palette, lightweight chiffon fabric with subtle ethnic embroidery, photographed on a model with natural outdoor lighting, editorial fashion magazine style"

These prompts are specifically crafted to work well with AI image generation tools and produce high-quality fashion imagery.
import warnings
warnings.filterwarnings('ignore', category=FutureWarning, module='google.generativeai')

import google.generativeai as genai
from config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)

class GeminiService:
    """Generate fashion recommendations using Google Gemini API"""
    
    def __init__(self):
        """Initialize Gemini API"""
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=Config.GEMINI_API_KEY)
        # Use the latest available model
        self.model = genai.GenerativeModel('models/gemini-flash-latest')
    
    def create_dress_generation_prompt(self, analysis_data, personalization=None):
        """
        Create detailed prompt for dress design generation
        
        Args:
            analysis_data: Dict containing body_shape, face_shape, skin_tone, undertone, colors
            personalization: Optional dict with mood, occasion, weather, budget
        
        Returns:
            str: Formatted prompt for dress generation
        """
        base_prompt = f"""You are a professional fashion designer AI specializing in dress creation. Based on the following analysis, create detailed dress design prompts for image generation.

PHYSICAL ATTRIBUTES:
- Body Shape: {analysis_data.get('body_shape', 'unknown')}
- Face Shape: {analysis_data.get('face_shape', 'unknown')}
- Skin Tone: {analysis_data.get('skin_tone', 'unknown')}
- Undertone: {analysis_data.get('undertone', 'unknown')}
- Current Dominant Colors: {', '.join(analysis_data.get('dominant_colors', []))}

"""

        # Add personalization if provided
        if personalization:
            base_prompt += "PERSONALIZATION CONTEXT:\n"
            if personalization.get('mood'):
                base_prompt += f"- Mood/Style Preference: {personalization['mood']}\n"
            if personalization.get('occasion'):
                base_prompt += f"- Occasion: {personalization['occasion']}\n"
            if personalization.get('weather'):
                base_prompt += f"- Weather Conditions: {personalization['weather']}\n"
            if personalization.get('budget'):
                base_prompt += f"- Budget Level: {personalization['budget']}\n"
            base_prompt += "\n"
        
        base_prompt += """Create 3 detailed dress design prompts optimized for this person. Each prompt should be comprehensive enough for image generation AI.

For each dress design, provide:

1. DESIGN STYLE: Overall aesthetic (e.g., "elegant A-line cocktail dress", "bohemian maxi dress")
2. SILHOUETTE: Body shape considerations (how it flatters their figure)
3. NECKLINE: Face shape complementary style
4. SLEEVES: Appropriate length/style
5. FABRIC: Suitable materials and textures
6. COLOR SCHEME: Specific colors that complement their skin tone
7. PATTERN/DETAILS: Embellishments, prints, or design elements
8. LENGTH: Appropriate length for their height/body proportion
9. FIT: How it should fit their body shape
10. ACCESSORIES: Suggested complementary accessories

Format your response as JSON with this exact structure:
{
  "dress_designs": [
    {
      "design_name": "Descriptive name of the dress",
      "design_style": "Overall aesthetic description",
      "silhouette": "Body-flattering shape description",
      "neckline": "Face-complementing neckline style",
      "sleeves": "Sleeve style and length",
      "fabric": "Recommended materials",
      "color_scheme": ["color1", "color2", "color3"],
      "pattern_details": "Embellishments or patterns",
      "length": "Dress length description",
      "fit": "How it fits the body shape",
      "accessories": ["accessory1", "accessory2"],
      "image_generation_prompt": "Detailed prompt for image generation AI like DALL-E, Midjourney, or Stable Diffusion"
    }
  ]
}

Make the image_generation_prompt very detailed and specific, including:
- Style and era (e.g., "modern elegant", "vintage 1950s")
- Specific design elements
- Color details
- Fabric texture descriptions
- Lighting and photography style
- Professional fashion photography context

Provide only the JSON response, no additional text."""

        return base_prompt

    def generate_dress_prompts(self, analysis_data, personalization=None):
        """
        Generate dress design prompts for image generation
        
        Args:
            analysis_data: Physical attribute analysis
            personalization: Optional personalization parameters
        
        Returns:
            dict: Dress design prompts
        """
        import json
        
        try:
            # Create dress generation prompt
            prompt = self.create_dress_generation_prompt(analysis_data, personalization)
            
            logger.info("Sending dress generation request to Gemini API...")
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            # Parse response
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            # Parse JSON
            dress_prompts = json.loads(response_text.strip())
            
            logger.info("Successfully generated dress design prompts")
            return dress_prompts
        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse dress generation response: {str(e)}")
            if 'response_text' in locals():
                logger.error(f"Response text: {response_text}")
            
            # Return fallback structure
            return {
                "dress_designs": [
                    {
                        "design_name": "Flattering A-line Dress",
                        "design_style": "Classic elegant silhouette",
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
            }
        
        except Exception as e:
            logger.error(f"Error generating dress prompts: {str(e)}")
            raise
    def create_prompt(self, analysis_data, personalization=None):
        """
        Create detailed prompt for Gemini
        
        Args:
            analysis_data: Dict containing body_shape, face_shape, skin_tone, undertone, colors
            personalization: Optional dict with mood, occasion, weather, budget
        
        Returns:
            str: Formatted prompt
        """
        base_prompt = f"""You are a professional fashion stylist AI. Based on the following analysis of a person's physical attributes, provide personalized fashion recommendations.

PHYSICAL ATTRIBUTES:
- Body Shape: {analysis_data.get('body_shape', 'unknown')}
- Face Shape: {analysis_data.get('face_shape', 'unknown')}
- Skin Tone: {analysis_data.get('skin_tone', 'unknown')}
- Undertone: {analysis_data.get('undertone', 'unknown')}
- Current Dominant Colors: {', '.join(analysis_data.get('dominant_colors', []))}

"""

        # Add personalization if provided
        if personalization:
            base_prompt += "PERSONALIZATION:\n"
            if personalization.get('mood'):
                base_prompt += f"- Mood: {personalization['mood']}\n"
            if personalization.get('occasion'):
                base_prompt += f"- Occasion: {personalization['occasion']}\n"
            if personalization.get('weather'):
                base_prompt += f"- Weather: {personalization['weather']}\n"
            if personalization.get('budget'):
                base_prompt += f"- Budget: {personalization['budget']}\n"
            base_prompt += "\n"
        
        base_prompt += """Please provide:

1. RECOMMENDED OUTFIT CATEGORIES (list 4-5 specific outfit types that would flatter this body and face shape)
2. RECOMMENDED COLOR PALETTE (list 6-8 specific colors with hex codes that complement this skin tone and undertone)
3. STYLING TIPS (provide 3-4 actionable styling tips considering all attributes)

Format your response as JSON with this exact structure:
{
  "recommended_categories": ["category1", "category2", ...],
  "recommended_colors": [
    {"name": "color_name", "hex": "#hexcode"},
    ...
  ],
  "styling_tips": ["tip1", "tip2", ...]
}

Provide only the JSON response, no additional text."""

        return base_prompt
    
    def generate_recommendations(self, analysis_data, personalization=None):
        """
        Generate fashion recommendations
        
        Args:
            analysis_data: Physical attribute analysis
            personalization: Optional personalization parameters
        
        Returns:
            dict: Recommendations
        """
        import json  # Move import to function level
        
        try:
            # Create prompt
            prompt = self.create_prompt(analysis_data, personalization)
            
            logger.info("Sending request to Gemini API...")
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            # Parse response
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            # Parse JSON
            recommendations = json.loads(response_text.strip())
            
            logger.info("Successfully generated recommendations")
            return recommendations
        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini response: {str(e)}")
            if 'response_text' in locals():
                logger.error(f"Response text: {response_text}")
            
            # Return fallback structure
            return {
                "recommended_categories": ["casual_wear", "smart_casual"],
                "recommended_colors": [
                    {"name": "navy_blue", "hex": "#000080"},
                    {"name": "white", "hex": "#FFFFFF"}
                ],
                "styling_tips": ["Focus on well-fitted clothing", "Experiment with accessories"]
            }
        
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            raise
    
    def generate_personalized_recommendations(self, analysis_data, personalization):
        """
        Generate recommendations with personalization
        
        Args:
            analysis_data: Physical attribute analysis
            personalization: Personalization parameters (mood, occasion, weather, budget)
        
        Returns:
            dict: Personalized recommendations
        """
        return self.generate_recommendations(analysis_data, personalization)

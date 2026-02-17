import cv2
import numpy as np
from sklearn.cluster import KMeans
from utils.logger import setup_logger

logger = setup_logger(__name__)

class ColorAnalyzer:
    """Analyze skin tone, undertone, and dominant colors"""
    
    @staticmethod
    def extract_skin_region(rgb_image):
        """
        Extract skin regions from image using color-based segmentation
        
        Args:
            rgb_image: Image in RGB format
        
        Returns:
            numpy.ndarray: Mask of skin regions
        """
        # Convert to YCrCb color space (better for skin detection)
        ycrcb = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2YCrCb)
        
        # Define skin color range in YCrCb
        lower = np.array([0, 133, 77], dtype=np.uint8)
        upper = np.array([255, 173, 127], dtype=np.uint8)
        
        # Create mask
        skin_mask = cv2.inRange(ycrcb, lower, upper)
        
        # Apply morphological operations to clean up mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_CLOSE, kernel)
        skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, kernel)
        
        return skin_mask
    
    @staticmethod
    def get_dominant_color(image, mask=None, n_colors=1):
        """
        Extract dominant colors using K-means clustering
        
        Args:
            image: RGB image
            mask: Optional mask to restrict analysis
            n_colors: Number of dominant colors to extract
        
        Returns:
            list: RGB values of dominant colors
        """
        # Reshape image to be a list of pixels
        pixels = image.reshape(-1, 3)
        
        # Apply mask if provided
        if mask is not None:
            mask_flat = mask.reshape(-1)
            pixels = pixels[mask_flat > 0]
        
        # Need at least some pixels
        if len(pixels) < 10:
            logger.warning("Not enough pixels for color analysis")
            return [(128, 128, 128)] * n_colors
        
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
        kmeans.fit(pixels)
        
        # Get cluster centers (dominant colors)
        colors = kmeans.cluster_centers_.astype(int)
        
        return [tuple(color) for color in colors]
    
    @staticmethod
    def classify_skin_tone(rgb_color):
        """
        Classify skin tone based on RGB value
        
        Args:
            rgb_color: RGB tuple
        
        Returns:
            str: Skin tone category
        """
        r, g, b = rgb_color
        
        # Calculate brightness (perceived luminance)
        brightness = (0.299 * r + 0.587 * g + 0.114 * b)
        
        # Classify based on brightness
        if brightness > 200:
            return "very_light"
        elif brightness > 170:
            return "light"
        elif brightness > 130:
            return "medium"
        elif brightness > 90:
            return "tan"
        elif brightness > 60:
            return "dark"
        else:
            return "very_dark"
    
    @staticmethod
    def detect_undertone(rgb_color):
        """
        Estimate skin undertone (warm/cool/neutral)
        
        Args:
            rgb_color: RGB tuple
        
        Returns:
            str: Undertone (warm, cool, neutral)
        """
        r, g, b = rgb_color
        
        # Calculate color temperature indicators
        warm_indicator = r - b  # Red vs Blue
        yellow_indicator = (r + g) / 2 - b  # Yellow vs Blue
        
        # Classify undertone
        if warm_indicator > 25 and yellow_indicator > 20:
            return "warm"
        elif warm_indicator < -10 and yellow_indicator < -5:
            return "cool"
        else:
            return "neutral"
    
    @staticmethod
    def rgb_to_hex(rgb_color):
        """
        Convert RGB to hex color code
        
        Args:
            rgb_color: RGB tuple
        
        Returns:
            str: Hex color code
        """
        return "#{:02x}{:02x}{:02x}".format(*rgb_color)
    
    def analyze(self, rgb_image):
        """
        Perform complete color analysis
        
        Args:
            rgb_image: Image in RGB format
        
        Returns:
            dict: Color analysis results
        """
        try:
            # Extract skin regions
            skin_mask = self.extract_skin_region(rgb_image)
            
            # Get dominant skin color
            skin_colors = self.get_dominant_color(rgb_image, skin_mask, n_colors=1)
            dominant_skin = skin_colors[0]
            
            # Classify skin tone and undertone
            skin_tone = self.classify_skin_tone(dominant_skin)
            undertone = self.detect_undertone(dominant_skin)
            
            # Get dominant clothing colors (excluding skin regions)
            clothing_mask = cv2.bitwise_not(skin_mask)
            clothing_colors = self.get_dominant_color(rgb_image, clothing_mask, n_colors=3)
            
            # Convert to hex
            clothing_hex = [self.rgb_to_hex(color) for color in clothing_colors]
            
            logger.info(f"Color analysis complete - Skin: {skin_tone}, Undertone: {undertone}")
            
            return {
                "skin_tone": skin_tone,
                "undertone": undertone,
                "dominant_colors": clothing_hex
            }
        
        except Exception as e:
            logger.error(f"Error in color analysis: {str(e)}")
            return {
                "skin_tone": "unknown",
                "undertone": "unknown",
                "dominant_colors": []
            }

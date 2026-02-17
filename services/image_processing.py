import cv2
import numpy as np
from PIL import Image
from config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)

class ImageProcessor:
    """Handle image validation, loading, and preprocessing"""
    
    @staticmethod
    def load_image(image_path):
        """
        Load image from file path
        
        Args:
            image_path: Path to image file
        
        Returns:
            numpy.ndarray: Image in BGR format (OpenCV)
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError("Failed to load image")
            
            logger.info(f"Image loaded successfully: {image.shape}")
            return image
        
        except Exception as e:
            logger.error(f"Error loading image: {str(e)}")
            raise
    
    @staticmethod
    def resize_image(image, max_width=None, max_height=None):
        """
        Resize image while maintaining aspect ratio
        
        Args:
            image: OpenCV image (numpy array)
            max_width: Maximum width
            max_height: Maximum height
        
        Returns:
            numpy.ndarray: Resized image
        """
        if max_width is None:
            max_width = Config.IMAGE_MAX_WIDTH
        if max_height is None:
            max_height = Config.IMAGE_MAX_HEIGHT
        
        height, width = image.shape[:2]
        
        # Calculate scaling factor
        width_scale = max_width / width
        height_scale = max_height / height
        scale = min(width_scale, height_scale, 1.0)  # Don't upscale
        
        if scale < 1.0:
            new_width = int(width * scale)
            new_height = int(height * scale)
            resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
            logger.info(f"Image resized from {width}x{height} to {new_width}x{new_height}")
            return resized
        
        return image
    
    @staticmethod
    def convert_to_rgb(image):
        """
        Convert BGR image to RGB
        
        Args:
            image: OpenCV image in BGR format
        
        Returns:
            numpy.ndarray: Image in RGB format
        """
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    @staticmethod
    def preprocess_for_mediapipe(image):
        """
        Prepare image for MediaPipe processing
        
        Args:
            image: OpenCV image (BGR)
        
        Returns:
            numpy.ndarray: RGB image ready for MediaPipe
        """
        # Resize if needed
        resized = ImageProcessor.resize_image(image)
        
        # Convert to RGB (MediaPipe requires RGB)
        rgb_image = ImageProcessor.convert_to_rgb(resized)
        
        return rgb_image
    
    @staticmethod
    def save_processed_image(image, output_path):
        """
        Save processed image to disk
        
        Args:
            image: OpenCV image
            output_path: Path to save image
        """
        try:
            cv2.imwrite(output_path, image)
            logger.info(f"Processed image saved to {output_path}")
        except Exception as e:
            logger.error(f"Error saving image: {str(e)}")
            raise

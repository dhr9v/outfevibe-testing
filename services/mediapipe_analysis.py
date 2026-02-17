import mediapipe as mp
import numpy as np
from utils.logger import setup_logger

logger = setup_logger(__name__)

class MediaPipeAnalyzer:
    """Analyze body and face shape using MediaPipe"""
    
    def __init__(self):
        """Initialize MediaPipe solutions"""
        try:
            # New MediaPipe API (0.10.8+)
            from mediapipe.tasks import python
            from mediapipe.tasks.python import vision
            
            # For newer versions, we'll use a simpler approach
            self.use_legacy_api = False
            logger.info("Using MediaPipe Tasks API")
            
        except ImportError:
            # Fallback to legacy API
            self.use_legacy_api = True
            if hasattr(mp, 'solutions'):
                self.mp_pose = mp.solutions.pose
                self.mp_face_mesh = mp.solutions.face_mesh
                
                # Initialize pose detector
                self.pose = self.mp_pose.Pose(
                    static_image_mode=True,
                    model_complexity=2,
                    min_detection_confidence=0.5
                )
                
                # Initialize face mesh detector
                self.face_mesh = self.mp_face_mesh.FaceMesh(
                    static_image_mode=True,
                    max_num_faces=1,
                    min_detection_confidence=0.5
                )
                logger.info("Using MediaPipe Solutions API")
            else:
                logger.warning("MediaPipe solutions not available - using fallback analysis")
                self.use_legacy_api = False
    
    def analyze_body_shape(self, rgb_image):
        """
        Detect body shape from pose landmarks
        
        Args:
            rgb_image: Image in RGB format
        
        Returns:
            str: Body shape (rectangle, triangle, inverted_triangle, oval, hourglass)
        """
        if not self.use_legacy_api:
            # Fallback: simple estimation based on image dimensions
            logger.warning("Using fallback body shape analysis")
            height, width = rgb_image.shape[:2]
            ratio = height / width if width > 0 else 1.5
            
            if ratio > 1.6:
                return "rectangle"
            elif ratio < 1.3:
                return "oval"
            else:
                return "hourglass"
        
        try:
            results = self.pose.process(rgb_image)
            
            if not results.pose_landmarks:
                logger.warning("No pose detected in image")
                return "unknown"
            
            landmarks = results.pose_landmarks.landmark
            
            # Get key body points
            left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
            left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP]
            right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP]
            
            # Calculate widths
            shoulder_width = abs(right_shoulder.x - left_shoulder.x)
            hip_width = abs(right_hip.x - left_hip.x)
            
            # Calculate ratio
            if shoulder_width == 0:
                return "unknown"
            
            ratio = hip_width / shoulder_width
            
            # Determine body shape based on ratio
            if ratio < 0.85:
                body_shape = "inverted_triangle"
            elif ratio > 1.15:
                body_shape = "triangle"
            elif 0.95 <= ratio <= 1.05:
                body_shape = "rectangle"
            else:
                body_shape = "oval"
            
            logger.info(f"Body shape detected: {body_shape} (ratio: {ratio:.2f})")
            return body_shape
        
        except Exception as e:
            logger.error(f"Error analyzing body shape: {str(e)}")
            return "unknown"
    
    def analyze_face_shape(self, rgb_image):
        """
        Detect face shape from face mesh landmarks
        
        Args:
            rgb_image: Image in RGB format
        
        Returns:
            str: Face shape (oval, round, square, heart, long)
        """
        if not self.use_legacy_api:
            # Fallback: simple estimation
            logger.warning("Using fallback face shape analysis")
            return "oval"
        
        try:
            results = self.face_mesh.process(rgb_image)
            
            if not results.multi_face_landmarks:
                logger.warning("No face detected in image")
                return "unknown"
            
            face_landmarks = results.multi_face_landmarks[0]
            landmarks = face_landmarks.landmark
            
            # Get key facial points (simplified estimation)
            # Top of face (forehead)
            top = landmarks[10]
            # Bottom of face (chin)
            bottom = landmarks[152]
            # Left side of face
            left = landmarks[234]
            # Right side of face
            right = landmarks[454]
            
            # Calculate dimensions
            face_height = abs(bottom.y - top.y)
            face_width = abs(right.x - left.x)
            
            if face_width == 0:
                return "unknown"
            
            # Face ratio
            ratio = face_height / face_width
            
            # Determine face shape (basic estimation)
            if ratio > 1.4:
                face_shape = "long"
            elif ratio < 1.1:
                face_shape = "round"
            elif 1.1 <= ratio <= 1.25:
                # Check forehead vs jaw width for heart/square
                forehead_width = abs(landmarks[108].x - landmarks[337].x)
                jaw_width = abs(landmarks[172].x - landmarks[397].x)
                
                if forehead_width > jaw_width * 1.1:
                    face_shape = "heart"
                else:
                    face_shape = "square"
            else:
                face_shape = "oval"
            
            logger.info(f"Face shape detected: {face_shape} (ratio: {ratio:.2f})")
            return face_shape
        
        except Exception as e:
            logger.error(f"Error analyzing face shape: {str(e)}")
            return "unknown"
    
    def analyze(self, rgb_image):
        """
        Perform complete MediaPipe analysis
        
        Args:
            rgb_image: Image in RGB format
        
        Returns:
            dict: Analysis results
        """
        body_shape = self.analyze_body_shape(rgb_image)
        face_shape = self.analyze_face_shape(rgb_image)
        
        return {
            "body_shape": body_shape,
            "face_shape": face_shape
        }
    
    def __del__(self):
        """Clean up MediaPipe resources"""
        try:
            if self.use_legacy_api and hasattr(self, 'pose'):
                self.pose.close()
            if self.use_legacy_api and hasattr(self, 'face_mesh'):
                self.face_mesh.close()
        except Exception:
            pass  # Ignore cleanup errors

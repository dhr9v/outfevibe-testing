import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

from config import Config
from utils import setup_logger, allowed_file, validate_file_size, sanitize_filename
from services import ImageProcessor, MediaPipeAnalyzer, ColorAnalyzer, GeminiService

# Initialize Flask app
app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config.from_object(Config)
Config.init_app(app)

# Enable CORS
CORS(app)

# Setup logger
logger = setup_logger(__name__)

# Initialize services
image_processor = ImageProcessor()
mediapipe_analyzer = MediaPipeAnalyzer()
color_analyzer = ColorAnalyzer()
gemini_service = GeminiService()


@app.route('/', methods=['GET'])
def index():
    """Serve the web interface"""
    return app.send_static_file('index.html')


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Outfevibe Vision AI',
        'version': '1.0.0'
    }), 200


@app.route('/analyze', methods=['POST'])
def analyze_fashion():
    """
    Main endpoint: Analyze uploaded image and generate fashion recommendations
    
    Expected: multipart/form-data with 'image' file
    
    Returns:
        JSON with complete analysis and recommendations
    """
    try:
        # Validate file presence
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: jpg, jpeg, png'}), 400
        
        # Validate file size
        if not validate_file_size(file):
            return jsonify({'error': f'File too large. Maximum size: {Config.MAX_FILE_SIZE / (1024*1024)}MB'}), 400
        
        # Save file temporarily
        filename = sanitize_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        logger.info(f"Processing image: {filename}")
        
        # STEP 1: Load and preprocess image
        image = image_processor.load_image(filepath)
        rgb_image = image_processor.preprocess_for_mediapipe(image)
        
        # STEP 2: MediaPipe Analysis (Body & Face Shape)
        mediapipe_results = mediapipe_analyzer.analyze(rgb_image)
        
        # STEP 3: Color Analysis (Skin Tone & Colors)
        color_results = color_analyzer.analyze(rgb_image)
        
        # STEP 4: Combine analysis results
        analysis_data = {
            **mediapipe_results,
            **color_results
        }
        
        logger.info(f"Analysis complete: {analysis_data}")
        
        # STEP 5: Generate AI recommendations using Gemini
        recommendations = gemini_service.generate_recommendations(analysis_data)
        
        # Clean up uploaded file
        os.remove(filepath)
        
        # STEP 6: Return complete response
        response = {
            'analysis': analysis_data,
            'recommendations': recommendations,
            'status': 'success'
        }
        
        logger.info("Request processed successfully")
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        
        # Clean up file if it exists
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/generate-dress-prompts', methods=['POST'])
def generate_dress_prompts():
    """
    Generate detailed dress design prompts for image generation
    
    Expected: multipart/form-data with 'image' file
    Optional form data: mood, occasion, weather, budget
    
    Returns:
        JSON with analysis, recommendations, and dress design prompts
    """
    try:
        # Validate file presence
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: jpg, jpeg, png'}), 400
        
        # Validate file size
        if not validate_file_size(file):
            return jsonify({'error': f'File too large. Maximum size: {Config.MAX_FILE_SIZE / (1024*1024)}MB'}), 400
        
        # Get personalization parameters from form data
        personalization = {
            'mood': request.form.get('mood'),
            'occasion': request.form.get('occasion'),
            'weather': request.form.get('weather'),
            'budget': request.form.get('budget')
        }
        
        # Remove None values
        personalization = {k: v for k, v in personalization.items() if v}
        
        # Save file temporarily
        filename = sanitize_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        logger.info(f"Generating dress prompts for: {filename}")
        logger.info(f"Personalization: {personalization}")
        
        # Process image
        image = image_processor.load_image(filepath)
        rgb_image = image_processor.preprocess_for_mediapipe(image)
        
        # Analyze
        mediapipe_results = mediapipe_analyzer.analyze(rgb_image)
        color_results = color_analyzer.analyze(rgb_image)
        
        analysis_data = {
            **mediapipe_results,
            **color_results
        }
        
        # Generate regular recommendations first
        recommendations = gemini_service.generate_recommendations(
            analysis_data,
            personalization
        )
        
        # Generate dress design prompts
        dress_prompts = gemini_service.generate_dress_prompts(
            analysis_data,
            personalization
        )
        
        # Clean up
        os.remove(filepath)
        
        response = {
            'analysis': analysis_data,
            'recommendations': recommendations,
            'personalization': personalization,
            'dress_prompts': dress_prompts,
            'status': 'success'
        }
        
        logger.info("Dress prompts generated successfully")
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Error generating dress prompts: {str(e)}")
        
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/personalize', methods=['POST'])
def personalize_recommendations():
    """
    BONUS: Generate personalized recommendations
    
    Expected JSON:
    {
        "image": (file upload),
        "mood": "string",
        "occasion": "string",
        "weather": "string",
        "budget": "string"
    }
    
    Returns:
        JSON with personalized recommendations
    """
    try:
        # Validate file presence
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: jpg, jpeg, png'}), 400
        
        if not validate_file_size(file):
            return jsonify({'error': f'File too large. Maximum size: {Config.MAX_FILE_SIZE / (1024*1024)}MB'}), 400
        
        # Get personalization parameters from form data
        personalization = {
            'mood': request.form.get('mood'),
            'occasion': request.form.get('occasion'),
            'weather': request.form.get('weather'),
            'budget': request.form.get('budget')
        }
        
        # Remove None values
        personalization = {k: v for k, v in personalization.items() if v}
        
        # Save file temporarily
        filename = sanitize_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        logger.info(f"Processing personalized request: {filename}")
        logger.info(f"Personalization: {personalization}")
        
        # Process image
        image = image_processor.load_image(filepath)
        rgb_image = image_processor.preprocess_for_mediapipe(image)
        
        # Analyze
        mediapipe_results = mediapipe_analyzer.analyze(rgb_image)
        color_results = color_analyzer.analyze(rgb_image)
        
        analysis_data = {
            **mediapipe_results,
            **color_results
        }
        
        # Generate personalized recommendations
        recommendations = gemini_service.generate_personalized_recommendations(
            analysis_data,
            personalization
        )
        
        # Clean up
        os.remove(filepath)
        
        response = {
            'analysis': analysis_data,
            'personalization': personalization,
            'recommendations': recommendations,
            'status': 'success'
        }
        
        logger.info("Personalized request processed successfully")
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Error processing personalized request: {str(e)}")
        
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("🎨 Outfevibe Vision AI - Starting Server")
    logger.info("=" * 60)
    logger.info(f"Server running on: http://{Config.HOST}:{Config.PORT}")
    logger.info(f"Web Interface: http://localhost:{Config.PORT}")
    logger.info(f"Health Check: http://localhost:{Config.PORT}/health")
    logger.info("=" * 60)
    logger.info("Press CTRL+C to stop the server")
    logger.info("=" * 60)
    
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=(Config.FLASK_ENV == 'development')
    )

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import sys
import json
from bson import ObjectId
from datetime import datetime
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
# Import chatbot routes
from routes.chatbot_routes import chatbot_bp
# Import loan chatbot routes
from routes.loan_chatbot_routes import loan_chatbot_bp
from routes.calculator_routes import calculator_bp

# Register the loan chatbot blueprint after your other blueprints

# Register blueprints

# Load environment variables from .env file
load_dotenv()

# Add the current directory to the path to fix import issues
sys.path.append('.')

# Now import application modules
from routes.loan_routes import loan_bp
from routes.document_routes import document_bp
from routes.user_routes import user_bp
from routes.auth_routes import auth_bp
from utils.swagger import init_swagger
from create_default_user import create_default_user

def setup_logging(app):
    """Configure logging for the application."""
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Set up file handler for detailed logs
    file_handler = RotatingFileHandler(
        'logs/los.log',
        maxBytes=10240,  # 10KB per file
        backupCount=10    # Keep 10 backup files
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    
    # Set up console handler for immediate feedback
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    console_handler.setLevel(logging.INFO)

    # Add handlers to app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)
    
    # Initial log message
    app.logger.info('Loan Origination System startup')

    # Log some basic application info
    app.logger.info(f"Application running in {'debug' if app.debug else 'production'} mode")
    app.logger.info(f"Database host: {os.getenv('MONGODB_URI', 'default_connection')}")

class MongoJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(MongoJSONEncoder, self).default(obj)

# Create Flask app
app = Flask(__name__)

# Set up logging
setup_logging(app)

# Configure the app to use our custom JSON encoder
app.json_encoder = MongoJSONEncoder

# Configure CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Register blueprints
app.register_blueprint(loan_bp, url_prefix='/api/loans')
app.register_blueprint(document_bp, url_prefix='/api/documents')
app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')
app.register_blueprint(loan_chatbot_bp, url_prefix='/api/loan-chatbot')
app.register_blueprint(calculator_bp, url_prefix='/api/calculator')

# Initialize Swagger
init_swagger(app)

# Error handling with logging
@app.errorhandler(404)
def not_found(error):
    app.logger.warning(f"404 error: {request.url}")
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(error):
    app.logger.error(f"500 error: {str(error)}", exc_info=True)
    return jsonify({"error": "Internal server error"}), 500

# Root route for health check
@app.route('/')
def index():
    app.logger.info("Health check endpoint accessed")
    return jsonify({
        "status": "Loan Origination System API is running",
        "endpoints": {
            "auth": "/api/auth",
            "loans": "/api/loans",
            "documents": "/api/documents",
            "users": "/api/users",
            "swagger": "/api/swagger"
        }
    })

# Application configuration
app.config.update(
    MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max-limit
    SEND_FILE_MAX_AGE_DEFAULT=0
)

if __name__ == '__main__':
    # Create default user
    create_default_user()
    
    # Get port from environment variable or default to 8000
    port = int(os.environ.get('PORT', 8000))
    
    app.logger.info(f"Starting server on port {port}")
    
    # Run the app
    app.run(host='0.0.0.0', port=port, debug=True)

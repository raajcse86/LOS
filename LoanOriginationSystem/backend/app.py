from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import sys
import json
from bson import ObjectId
from datetime import datetime
from dotenv import load_dotenv

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

# Create a custom JSON encoder to handle MongoDB ObjectId serialization
class MongoJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(MongoJSONEncoder, self).default(obj)

# Create Flask app
app = Flask(__name__)

# Configure the app to use our custom JSON encoder
app.json_encoder = MongoJSONEncoder

# Configure CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Register blueprints
app.register_blueprint(loan_bp, url_prefix='/api/loans')
app.register_blueprint(document_bp, url_prefix='/api/documents')
app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(auth_bp, url_prefix='/api/auth')

# Initialize Swagger
init_swagger(app)

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500

# Root route for health check
@app.route('/')
def index():
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

if __name__ == '__main__':
    # Create default user
    create_default_user()
    
    # Get port from environment variable or default to 8000
    port = int(os.environ.get('PORT', 8000))
    
    # Run the app
    app.run(host='0.0.0.0', port=port, debug=True)

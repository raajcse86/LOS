from flask import Blueprint, request, jsonify
from utils.db import get_db

# Create a blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login/', methods=['POST'])
def login():
    """Login route for users."""
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password are required'}), 400
    
    username = data['username']
    password = data['password']
    
    # Connect to the database
    db = get_db()
    
    # Find the user
    user = db.users.find_one({'username': username})
    
    # Check if user exists and password matches
    if user and password == user.get('password'):  # In a real app, use password hashing
        # Convert ObjectId to string for JSON serialization
        user['_id'] = str(user['_id'])
        
        # Remove the password from the response
        user.pop('password', None)
        
        return jsonify(user), 200
    
    return jsonify({'error': 'Invalid username or password'}), 401

@auth_bp.route('/logout/', methods=['POST'])
def logout():
    """Logout route for users (client-side only for now)."""
    return jsonify({'message': 'Logged out successfully'}), 200
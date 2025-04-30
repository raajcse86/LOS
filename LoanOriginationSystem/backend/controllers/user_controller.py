from flask import jsonify, request
from services.user_service import UserService

user_service = UserService()

def get_all_users():
    """Get all users."""
    users = user_service.get_all_users()
    return jsonify(users)

def get_user(user_id):
    """Get a user by ID."""
    user = user_service.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

def get_users_by_role(role):
    """Get users by role."""
    users = user_service.get_users_by_role(role)
    return jsonify(users)

def create_user():
    """Create a new user."""
    data = request.json
    
    # Validate required fields
    required_fields = ['username', 'firstName', 'lastName', 'email', 'role']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400
    
    # Validate role
    valid_roles = ['Sales', 'Processor', 'Underwriter', 'Closer', 'Manager']
    if data['role'] not in valid_roles:
        return jsonify({"error": f"Invalid role. Must be one of: {', '.join(valid_roles)}"}), 400
    
    # Create user
    user = user_service.create_user(data)
    if not user:
        return jsonify({"error": "Failed to create user"}), 500
    
    return jsonify(user), 201

def update_user(user_id):
    """Update a user."""
    data = request.json
    
    # Validate role if provided
    if 'role' in data:
        valid_roles = ['Sales', 'Processor', 'Underwriter', 'Closer', 'Manager']
        if data['role'] not in valid_roles:
            return jsonify({"error": f"Invalid role. Must be one of: {', '.join(valid_roles)}"}), 400
    
    # Update user
    user = user_service.update_user(user_id, data)
    if not user:
        return jsonify({"error": "User not found or failed to update"}), 404
    
    return jsonify(user)

def delete_user(user_id):
    """Delete a user."""
    success = user_service.delete_user(user_id)
    if not success:
        return jsonify({"error": "User not found or failed to delete"}), 404
    
    return jsonify({"message": "User deleted successfully"})

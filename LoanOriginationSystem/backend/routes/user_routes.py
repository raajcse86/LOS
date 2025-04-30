from flask import Blueprint
import sys
import os

# Add the current directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controllers.user_controller import (
    get_all_users, get_user, get_users_by_role,
    create_user, update_user, delete_user
)

user_bp = Blueprint('user_bp', __name__)

# Get all users
user_bp.route('/', methods=['GET'])(get_all_users)

# Get a user by ID
user_bp.route('/<user_id>/', methods=['GET'])(get_user)

# Get users by role
user_bp.route('/role/<role>/', methods=['GET'])(get_users_by_role)

# Create a new user
user_bp.route('/', methods=['POST'])(create_user)

# Update a user
user_bp.route('/<user_id>/', methods=['PUT'])(update_user)

# Delete a user
user_bp.route('/<user_id>/', methods=['DELETE'])(delete_user)

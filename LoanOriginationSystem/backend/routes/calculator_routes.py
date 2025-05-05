from flask import Blueprint
from controllers.calculator_controller import calculator_chat

# Create a blueprint for calculator routes
calculator_bp = Blueprint('calculator', __name__)

# Calculator chat message endpoint
calculator_bp.route('/message', methods=['POST'])(calculator_chat) 
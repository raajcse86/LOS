from flask import Blueprint
from controllers.chatbot_controller import chat_message, create_chatbot_application

# Create a blueprint for chatbot routes
chatbot_bp = Blueprint('chatbot', __name__)

# Chat message endpoint
chatbot_bp.route('/message', methods=['POST'])(chat_message)

# Create application endpoint
chatbot_bp.route('/create-application', methods=['POST'])(create_chatbot_application)
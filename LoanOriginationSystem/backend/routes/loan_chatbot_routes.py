from flask import Blueprint
from controllers.loan_chatbot_controller import loan_chat_message

# Create a blueprint for loan chatbot routes
loan_chatbot_bp = Blueprint('loan_chatbot', __name__)

# Loan chat message endpoint
loan_chatbot_bp.route('/message', methods=['POST'])(loan_chat_message)
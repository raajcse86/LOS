from dotenv import load_dotenv
from flask import request, jsonify
import json
import os

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
chat = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GOOGLE_API_KEY)

def get_simple_response(user_message, conversation_history):
    """
    A simple placeholder function that returns predefined responses.
    This will be replaced with your LLM implementation.
    """
    # Simple responses based on user message
    if "name" in user_message.lower():
        return "Thank you for sharing your name! What's your email address?"
    elif "email" in user_message.lower():
        return "Got your email. What's your phone number?"
    elif "phone" in user_message.lower():
        return "Thanks! What's your estimated credit score?"
    elif "credit" in user_message.lower():
        return "What type of property are you looking to finance? (e.g., Single Family, Condo, Multi-Family)"
    elif "property" in user_message.lower():
        return "What's your estimated purchase price?"
    elif "price" in user_message.lower() or "purchase" in user_message.lower():
        return "How much down payment are you planning to make?"
    elif "down payment" in user_message.lower():
        return "What's your annual income?"
    elif "income" in user_message.lower():
        return "Thanks for providing all this information! I'll create a loan application for you. Would you like to proceed?"
    elif "yes" in user_message.lower() or "proceed" in user_message.lower() or "ok" in user_message.lower():
        return "Great! I've submitted your loan application. Our team will review it and contact you soon."
    else:
        return "I'm here to help with your loan application. Could you provide more details about what you're looking for?"


# This is the function that you'll replace with your LLM implementation
def get_llm_response(user_message, conversation_history):
    """
    Gets a response from a simple placeholder function.
    Replace this with your LLM implementation.
    """
    loan_appchat_prompt = f"""
    You are an intelligent loan application assistant. You're collecting loan information from a user by asking a fixed sequence of questions and tracking their answers.

You are given two inputs:
1. conversation_history – a JSON object containing key-value pairs of previously answered questions.
2. user_message – the latest message from the user, which may be an answer to the current question, a correction to a previous answer, or a confirmation.

conversation_history:
{conversation_history}

user_message:
{user_message}


Each time you're called, follow this process:

1. Look at conversation history to identify what questions have already been answered.
2. Ask the next question from the following list (in order):

   - What is your name?
   - What's your email address?
   - What's your phone number?
   - What's your estimated credit score?
   - What type of property are you looking to finance? (e.g., Single Family, Condo, Multi-Family)
   - What's your estimated purchase price?
   - How much down payment are you planning to make?
   - What's your annual income?

- The user_message may contain questions regarding what you are asking, if asked respond with the proper answer. Only go the next question from above if the user actually answers it properly.

- Once all the above questions are answered, **summarize** the collected information in a friendly format and ask:
  > Is everything correct? If you'd like to change anything, just tell me what to update.

- If `user_message` contains a correction (e.g., "Actually, my credit score is 680"), intelligently update the corresponding value in `conversation_history` and re-summarize with the update reflected.


Important note:
- Unless and Until its the last question from the list the response should only contain the current question in hand and the reason why you are asking that question in the loan application, You dont need to add what was already answered previously
- Once all the above questions from the list are answered, **summarize** the collected information in a friendly format and ask:
  > Is everything correct? If you'd like to change anything, just tell me what to update.

Output should contain:
- Only the question in hand and the reason you are asking the question in normal text

for example :

The output should not have:

Okay, I understand the instructions. Given the `conversation_history`: ```json ['text': 'My name is sharan', 'isUser': True] ``` and the `user_message`: ``` My name is sharan ``` The first question, "What is your name?" seems to be answered in both the conversation history and user message. So, the next question to ask is: What's your email address? I need this to keep you updated on your loan application status and to send you important documents.

Instead the output should only have
What's your email address? I need this to keep you updated on your loan application status and to send you important documents.
 meaning it should only have the question to ask part
    """
    response = chat([HumanMessage(content=loan_appchat_prompt)])

    # Log the received message and conversation history for debugging
    print(f"User message: {user_message}")
    print(f"Conversation history: {conversation_history}")

    # Currently using a simple placeholder - you'll replace this with your LLM code
    return response.content


def chat_message():
    """
    Handle a chatbot message.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        user_message = data.get('message', '')
        conversation_history = data.get('conversation_history', [])

        # Get response from LLM (or the placeholder function for now)
        response = get_llm_response(user_message, conversation_history)

        return jsonify({
            "response": response,
            "success": True
        }), 200
    except Exception as e:
        print(f"Error in chat_message: {e}")
        return jsonify({"error": str(e)}), 500


def create_chatbot_application():
    """
    Create a loan application from chatbot data.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # This is where you would process the application data
        # and create a loan application in your database
        print(f"Creating loan application from chatbot data: {data}")

        # For now, just return success
        return jsonify({
            "message": "Loan application created successfully",
            "success": True,
            "application_id": "temp_id_123"  # In production, this would be a real ID
        }), 201
    except Exception as e:
        print(f"Error in create_chatbot_application: {e}")
        return jsonify({"error": str(e)}), 500

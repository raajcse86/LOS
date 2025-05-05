import os

from dotenv import load_dotenv
from flask import request, jsonify
import json

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.db import get_db
from bson import ObjectId


load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
chat = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GOOGLE_API_KEY)

def get_loan_data(loan_id):
    """
    Get comprehensive loan data including documents for a specific loan.
    This will be used to provide context to the LLM.
    """
    try:
        db = get_db()

        # Get loan details
        loan_data = db.loans.find_one({"_id": ObjectId(loan_id)})
        if not loan_data:
            return None

        # Convert ObjectId to string for JSON serialization
        loan_data['_id'] = str(loan_data['_id'])

        # Get documents associated with this loan
        documents = list(db.documents.find({"loan_id": loan_id}))
        for doc in documents:
            doc['_id'] = str(doc['_id'])

        # Create a comprehensive loan context
        loan_context = {
            "loan": loan_data,
            "documents": documents
        }

        # Log the entire context for debugging and later LLM integration
        print(f"Loan context for LLM: {json.dumps(loan_context, indent=2)}")

        return loan_context
    except Exception as e:
        print(f"Error getting loan data: {str(e)}")
        return None



def get_llm_response(user_message,conversation_history,loan_application):
    loan_chat_prompt=f"""
    You are an intelligent, context-aware Loan Assistant. You are helping users throughout their loan application process by answering questions, offering suggestions, and guiding them to improve their chances of loan approval.
    
    You are provided with the following:
    1. user_message: the latest message from the user (a natural language question, concern, or follow-up).
    2. conversation_history: a list of past messages between you and the user to help maintain context.
    3. loan_application: a JSON object containing the user's complete loan application data (e.g., Name, Email, Credit Score, Property Type, Income, Purchase Price, Down Payment, etc.).
    
    user_message:
    {user_message}
    
    conversation_history:
    {conversation_history}
    
    loan_application:
    {loan_application}
    
    Your goals:
    - Understand the user’s intent from `user_message`, considering prior messages in `conversation_history`.
    - Respond naturally and informatively using the context and `loan_application` data.
    - Be empathetic and helpful. Explain things clearly.
    - If the user asks a question (e.g., “Am I eligible?”, “What’s missing?”, “How can I improve my loan offer?”):
      - Use the `loan_application` to give a detailed, relevant answer.
      - Highlight any missing, weak, or risky sections (e.g., low credit score, high DTI, small down payment).
      - Suggest improvements (e.g., increase down payment, improve credit score, add a co-applicant, etc.).
    - If the user gives an update or correction (e.g., “Change my income to 120000”), acknowledge the change, apply it mentally (or suggest applying it), and update your responses accordingly.
    - If the user is just chatting casually or has concerns (e.g., “I’m worried about approval”), provide helpful and kind responses that keep them engaged and informed.
    
    Only output what the user needs to hear in the current step — not everything.
    """
    response = chat([HumanMessage(content=loan_chat_prompt)])
    print(f" response from LLM for LoanChat controller is  ${response}")
    return response.content

def loan_chat_message():
    """
    Handle a loan-specific chatbot message.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        user_message = data.get('message', '')
        conversation_history = data.get('conversation_history', [])
        loan_id = data.get('loan_id')

        if not loan_id:
            return jsonify({
                "success": False,
                "error": "Loan ID is required"
            }), 400

        # Get comprehensive loan data
        loan_context = get_loan_data(loan_id)

        if not loan_context:
            return jsonify({
                "success": False,
                "error": "Loan not found"
            }), 404

        print(f"Loan chat - User message: {user_message}")
        print(f"Loan chat - Conversation history: {conversation_history}")

        # Get response using simple function (will be replaced with LLM)
        response = get_llm_response(user_message, conversation_history, loan_context)

        return jsonify({
            "success": True,
            "response": response
        }), 200
    except Exception as e:
        print(f"Error in loan_chat_message: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
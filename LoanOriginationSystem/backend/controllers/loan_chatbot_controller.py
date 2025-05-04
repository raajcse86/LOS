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


def get_simple_loan_response(user_message, conversation_history, loan_context):
    """
    A simple placeholder function that returns predefined responses based on the loan data.
    This will be replaced with your LLM implementation.
    """
    # Extract basic loan info for responses
    loan_data = loan_context.get("loan", {})
    borrower_info = loan_data.get("borrowerInfo", {})
    property_info = loan_data.get("propertyInfo", {})
    loan_pricing = loan_data.get("loanPricing", {})
    milestone = loan_data.get("milestone", "Unknown")

    # Simple response logic based on user query keywords
    if "status" in user_message.lower() or "progress" in user_message.lower():
        return f"This loan is currently in the {milestone} stage."

    elif "borrower" in user_message.lower() or "applicant" in user_message.lower() or "name" in user_message.lower():
        name = f"{borrower_info.get('firstName', '')} {borrower_info.get('lastName', '')}".strip()
        if name:
            return f"The borrower's name is {name}."
        else:
            return "I don't have the borrower's name on file."

    elif "property" in user_message.lower() or "home" in user_message.lower() or "house" in user_message.lower():
        if property_info:
            address = property_info.get("address", {})
            property_type = property_info.get("propertyType", "Not specified")
            if address:
                street = address.get("street", "")
                city = address.get("city", "")
                state = address.get("state", "")
                zipcode = address.get("zipCode", "")
                return f"The property is a {property_type} located at {street}, {city}, {state} {zipcode}."
            else:
                return f"The property is a {property_type}, but I don't have the address details."
        else:
            return "I don't have property information for this loan yet."

    elif "rate" in user_message.lower() or "interest" in user_message.lower():
        if loan_pricing:
            rate = loan_pricing.get("interestRate", "Not specified")
            return f"The interest rate for this loan is {rate}%."
        else:
            return "I don't have interest rate information for this loan yet."

    elif "amount" in user_message.lower() or "loan amount" in user_message.lower() or "borrow" in user_message.lower():
        if loan_pricing:
            amount = loan_pricing.get("loanAmount", "Not specified")
            return f"The loan amount is ${amount:,}."
        else:
            return "I don't have loan amount information yet."

    elif "document" in user_message.lower() or "upload" in user_message.lower() or "file" in user_message.lower():
        documents = loan_context.get("documents", [])
        if documents:
            doc_count = len(documents)
            doc_types = [doc.get("document_type") for doc in documents]
            return f"There are {doc_count} documents associated with this loan: {', '.join(doc_types)}."
        else:
            return "There are no documents uploaded for this loan yet."

    # Default response
    return "I'm your loan assistant. You can ask me about the loan status, borrower information, property details, interest rate, or documents."

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
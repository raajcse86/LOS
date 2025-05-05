from typing import Dict
from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from .calculator_agent import AgentState

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def multiplication_agent(state: AgentState) -> Dict:
    # Initialize Gemini model
    chat = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
    
    # Get the numbers from state
    numbers = state.numbers
    
    # Create the prompt for multiplication
    prompt = f"""
    You are a Multiplication AI Agent. Your task is to:
    1. Multiply the numbers: {numbers}
    2. Provide a friendly explanation of the multiplication process
    3. Return the result

    Previous conversation context:
    {[msg.content for msg in state.messages[-3:] if msg]}
    """
    
    # Get response from the model
    response = chat([prompt])
    response_text = response.content
    
    # Calculate the result
    result = 1
    for num in numbers:
        result *= num
    
    # Create a friendly response
    final_response = f"""
    Let me help you with the multiplication!
    Numbers to multiply: {numbers}
    Result: {result}
    
    {response_text}
    """
    
    # Update state
    state.result = result
    state.add_message(AIMessage(content=final_response))
    
    # Clear numbers for next operation
    state.numbers = []
    
    return {"next": "CALCULATE"} 
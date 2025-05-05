from typing import Dict, TypedDict, List
from langchain_core.messages import AIMessage, BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Define the state schema
class CalculatorState(TypedDict, total=False):
    messages: List[BaseMessage]
    next_step: str
    operation: str | None
    numbers: List[float]
    result: float | None
    next: str  # Added for routing
    completed_calculation: bool  # Track if we just completed a calculation

def should_end(state: CalculatorState) -> bool:
    """Determine if we should end the conversation."""
    if not state["messages"]:
        return False
    
    last_message = state["messages"][-1].content.lower()
    end_phrases = ["thank", "bye", "goodbye", "quit", "exit"]
    return any(phrase in last_message for phrase in end_phrases)

def addition_agent(state: CalculatorState) -> CalculatorState:
    # Initialize Gemini model
    chat = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GOOGLE_API_KEY)
    
    # Check if we should end the conversation
    if should_end(state):
        state["next"] = END
        return state
    
    # Get the numbers from state
    numbers = state.get("numbers", [])
    messages = state["messages"]
    
    # Create the prompt for addition
    prompt = f"""
    You are an Addition AI Agent. Your task is to:
    1. Add the numbers: {numbers}
    2. Provide a friendly explanation of the addition process
    3. Return the result

    Previous conversation context:
    {[msg.content for msg in messages[-3:] if msg]}
    """
    
    # Get response from the model
    response = chat.invoke([prompt])
    response_text = response.content
    
    # Calculate the result
    result = sum(numbers)
    
    # Create a friendly response
    final_response = f"""
    Let me help you with the addition!
    Numbers to add: {numbers}
    Result: {result}
    
    {response_text}
    
    Would you like to perform another calculation? You can say 'bye' to end.
    """
    
    # Update messages with the response
    messages.append(AIMessage(content=final_response))
    
    # Create new state
    new_state = CalculatorState(
        messages=messages,
        next_step="CALCULATE",
        operation=None,
        numbers=[],  # Clear numbers for next operation
        result=result,
        completed_calculation=True,  # Mark that we just completed a calculation
        next="CALCULATE"
    )
    
    return new_state 
from typing import Dict, List, Tuple, Any, TypedDict, Union
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
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

# Calculator Agent
def calculator_agent(state: CalculatorState) -> CalculatorState:
    # Initialize Gemini model
    chat = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GOOGLE_API_KEY)
    
    # Get the last user message
    messages = state["messages"]
    last_message = messages[-1].content.lower() if messages else ""
    
    # Check for end conditions
    if "bye" in last_message or "thank" in last_message or "quit" in last_message or "exit" in last_message:
        state["next"] = END
        return state
    
    # If we just completed a calculation and the user has sent a new message
    if state.get("completed_calculation", False) and len(messages) > 1 and isinstance(messages[-1], HumanMessage):
        # Reset completed_calculation since we're starting a new one
        state["completed_calculation"] = False
    
    # Create the prompt for operation identification
    prompt = f"""
    You are a Calculator AI Agent. Analyze the user's input and determine:
    1. What mathematical operation is needed (addition or multiplication)
    2. Extract any numbers if present
    3. If numbers are not present, ask for them

    Current message: {last_message}
    Previous operation (if any): {state.get('operation')}
    Previous numbers (if any): {state.get('numbers', [])}
    Previous result (if any): {state.get('result')}

    Respond in a conversational way and determine the next step.
    If you find numbers in the message, include them in your response like this: NUMBERS_FOUND: [number1, number2, ...]
    """
    
    # Get response from the model
    response = chat.invoke([HumanMessage(content=prompt)])
    response_text = response.content
    
    # Add AI response to conversation history
    messages.append(AIMessage(content=response_text))
    
    # Extract numbers if present in the response
    numbers = state.get("numbers", [])
    if "NUMBERS_FOUND:" in response_text:
        try:
            numbers_str = response_text.split("NUMBERS_FOUND:")[1].split("\n")[0].strip()
            numbers = eval(numbers_str)  # Safely evaluate the array of numbers
        except:
            numbers = []
    
    # Simple operation detection logic
    operation = None
    if "add" in last_message or "plus" in last_message or "sum" in last_message:
        operation = "ADDITION"
    elif "multiply" in last_message or "times" in last_message or "product" in last_message:
        operation = "MULTIPLICATION"
    
    # Create updated state
    new_state = CalculatorState(
        messages=messages,
        next_step="CALCULATE",
        operation=operation,
        numbers=numbers,
        result=state.get("result"),
        completed_calculation=False
    )
    
    # Add routing information
    if operation and len(numbers) >= 2:
        new_state["next"] = operation
    else:
        new_state["next"] = "CALCULATE"
    
    return new_state

# Create the graph
def create_calculator_graph() -> StateGraph:
    # Create a new graph with the state schema
    workflow = StateGraph(CalculatorState)
    
    # Import the agent functions
    from .addition_agent import addition_agent
    from .multiplication_agent import multiplication_agent
    
    # Add all nodes
    workflow.add_node("CALCULATE", calculator_agent)
    workflow.add_node("ADDITION", addition_agent)
    workflow.add_node("MULTIPLICATION", multiplication_agent)
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "CALCULATE",
        lambda x: x["next"],
        {
            "ADDITION": "ADDITION",
            "MULTIPLICATION": "MULTIPLICATION",
            "CALCULATE": "CALCULATE",
            END: END
        }
    )
    
    # Add edges from operation nodes back to calculate
    workflow.add_edge("ADDITION", "CALCULATE")
    workflow.add_edge("MULTIPLICATION", "CALCULATE")
    
    # Set the entry point
    workflow.set_entry_point("CALCULATE")
    
    return workflow 
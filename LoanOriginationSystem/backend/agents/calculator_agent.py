from typing import Dict, List, Tuple, Any
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Define the state type
class AgentState:
    def __init__(self):
        self.messages: List[BaseMessage] = []
        self.next_step: str = "CALCULATE"
        self.operation: str = None
        self.numbers: List[float] = []
        self.result: float = None

    def add_message(self, message: BaseMessage):
        self.messages.append(message)

    def get_history(self) -> List[BaseMessage]:
        return self.messages

# Calculator Agent
def calculator_agent(state: AgentState) -> Dict:
    # Initialize Gemini model
    chat = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
    
    # Get the last user message
    last_message = state.messages[-1].content if state.messages else ""
    
    # Create the prompt for operation identification
    prompt = f"""
    You are a Calculator AI Agent. Analyze the user's input and determine:
    1. What mathematical operation is needed (addition or multiplication)
    2. Extract any numbers if present
    3. If numbers are not present, ask for them

    Current message: {last_message}
    Previous operation (if any): {state.operation}
    Previous numbers (if any): {state.numbers}
    Previous result (if any): {state.result}

    Respond in a conversational way and determine the next step.
    """
    
    # Get response from the model
    response = chat([HumanMessage(content=prompt)])
    response_text = response.content
    
    # Add AI response to conversation history
    state.add_message(AIMessage(content=response_text))
    
    # Simple operation detection logic
    if "add" in last_message.lower() or "plus" in last_message.lower() or "sum" in last_message.lower():
        state.operation = "ADDITION"
    elif "multiply" in last_message.lower() or "times" in last_message.lower() or "product" in last_message.lower():
        state.operation = "MULTIPLICATION"
    
    # Determine next step
    if state.operation and len(state.numbers) >= 2:
        return {"next": state.operation}
    else:
        return {"next": "CALCULATE"}

# Create the graph
def create_calculator_graph() -> StateGraph:
    # Create a new graph
    workflow = StateGraph(AgentState)
    
    # Add the calculator node
    workflow.add_node("CALCULATE", calculator_agent)
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "CALCULATE",
        lambda x: x["next"],
        {
            "ADDITION": "ADDITION",
            "MULTIPLICATION": "MULTIPLICATION",
            "CALCULATE": "CALCULATE",
        }
    )
    
    # Add edges from operation nodes back to calculate
    workflow.add_edge("ADDITION", "CALCULATE")
    workflow.add_edge("MULTIPLICATION", "CALCULATE")
    
    # Set the entry point
    workflow.set_entry_point("CALCULATE")
    
    return workflow 
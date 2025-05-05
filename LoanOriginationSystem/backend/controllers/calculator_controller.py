from flask import request, jsonify
from agents.calculator_agent import create_calculator_graph, AgentState
from langchain_core.messages import HumanMessage

def calculator_chat():
    """
    Handle calculator chatbot interactions.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        user_message = data.get('message', '')
        conversation_history = data.get('conversation_history', [])

        # Create or get the state
        state = AgentState()
        
        # Add conversation history to state
        for msg in conversation_history:
            if msg.get('isUser', False):
                state.add_message(HumanMessage(content=msg['text']))
        
        # Add current message to state
        state.add_message(HumanMessage(content=user_message))
        
        # Create and run the graph
        graph = create_calculator_graph()
        result = graph.invoke(state)
        
        # Get the latest AI message
        latest_response = result.messages[-1].content if result.messages else "I'm sorry, I couldn't process that."

        return jsonify({
            "response": latest_response,
            "success": True
        }), 200
        
    except Exception as e:
        print(f"Error in calculator_chat: {str(e)}")
        return jsonify({
            "error": str(e),
            "success": False
        }), 500 
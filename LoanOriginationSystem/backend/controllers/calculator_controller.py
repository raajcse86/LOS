from flask import request, jsonify
from agents.calculator_agent import create_calculator_graph, CalculatorState
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

        # Initialize messages list
        messages = []
        
        # Add conversation history to messages
        for msg in conversation_history:
            if msg.get('isUser', False):
                messages.append(HumanMessage(content=msg['text']))
        
        # Add current message to messages
        messages.append(HumanMessage(content=user_message))
        
        # Create initial state using CalculatorState
        initial_state = CalculatorState(
            messages=messages,
            next_step="CALCULATE",
            operation=None,
            numbers=[],
            result=None
        )
        
        # Create and run the graph
        graph = create_calculator_graph()
        app = graph.compile()  # Compile the graph
        
        # Run the graph with the proper state format
        result = app.invoke(initial_state)
        
        # Extract the latest AI message from the messages list
        latest_messages = result.get("messages", [])
        latest_response = latest_messages[-1].content if latest_messages else "I'm sorry, I couldn't process that."

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
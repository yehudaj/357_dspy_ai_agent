"""AI Agent for airline customer service using DSPy."""
import dspy
import mlflow
from config import get_openai_key
from tools import (
    fetch_flight_info,
    fetch_itinerary,
    pick_flight,
    book_flight,
    cancel_itinerary,
    get_user_info,
    file_ticket,
)

# Set up MLflow tracking with SQLite backend
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("dspy_airline_agent")


class DSPyAirlineCustomerService(dspy.Signature):
    """You are a helpful airline customer service agent that assists users with flight booking and travel questions.

    You should:
    1. Use your general knowledge to answer travel-related questions (destinations, weather, recommendations, etc.)
    2. Use the provided tools when you need to search flights, book tickets, or manage existing bookings
    3. Be conversational and helpful, providing recommendations based on user preferences
    4. Only use tools when you actually need to interact with the booking system
    
    Available destinations in our system: SFO, JFK, LAX, SNA, ORD, SEA, MIA, BOS, DEN
    """

    user_request: str = dspy.InputField()
    process_result: str = dspy.OutputField(
        desc=(
            "A helpful response that either: (1) answers the user's question using general knowledge about "
            "travel, destinations, and weather, OR (2) provides booking information after using tools to "
            "search/book flights. Include specific details like confirmation numbers when booking."
        )
    )


# Configure DSPy with OpenAI - using gpt-4 for better reasoning
lm = dspy.LM(model='openai/gpt-4o-mini', api_key=get_openai_key())
dspy.configure(lm=lm)

# Create the ReAct agent with max_iters to prevent excessive tool calling
agent = dspy.ReAct(
    DSPyAirlineCustomerService,
    tools=[
        fetch_flight_info,
        fetch_itinerary,
        pick_flight,
        book_flight,
        cancel_itinerary,
        get_user_info,
        file_ticket,
    ],
    max_iters=5  # Limit iterations to prevent endless loops
)


if __name__ == "__main__":
    # Example usage
    print("=== DSPy Airline Customer Service Agent ===\n")
    
    # Start MLflow run
    with mlflow.start_run():
        mlflow.log_param("model", "gpt-4o-mini")
        mlflow.log_param("agent_type", "ReAct")
        mlflow.log_param("max_iters", 5)
        
        while True:
            user_request = input("\nUser: ").strip()
            if not user_request or user_request.lower() in ['exit', 'quit', 'bye']:
                print("Thank you for using our service. Goodbye!")
                break
            
            # Log user request
            mlflow.log_param(f"request_{mlflow.active_run().info.run_id[:8]}", user_request[:100])
            
            result = agent(user_request=user_request)
            print(f"Agent: {result.process_result}")
            
            # Log response
            mlflow.log_metric("interactions", 1)
    # Test case: Book a flight
    

"""AI Agent for airline customer service using DSPy."""
import dspy
import mlflow
from config import get_openai_key
from tools import (
    get_available_destinations,
    get_all_destinations,
    search_routes,
    fetch_flight_info,
    fetch_itinerary,
    pick_flight,
    book_flight,
    cancel_itinerary,
    get_user_info,
    file_ticket,
)

# Set up MLflow tracking with SQLite backend
mlflow.set_tracking_uri("sqlite:///mlruns.db")
mlflow.set_experiment("airline-agent")

# Enable MLflow autologging for DSPy - this captures all traces automatically
mlflow.dspy.autolog()


class DSPyAirlineCustomerService(dspy.Signature):
    """You are a helpful airline customer service agent that assists users with flight booking and travel questions.

    You should:
    1. Use your general knowledge to answer travel-related questions and make recommendations based on user preferences
       (warm weather, adventure, culture, beaches, skiing, etc.) - YOU decide what destinations match their criteria
    2. Use the provided tools to discover what destinations we fly to, then match them to user preferences
    3. Use tools when you need to search flights, check routes, book tickets, or manage existing bookings
    4. Be conversational and helpful - leverage your knowledge about destinations, weather, activities, and travel
    
    Available destinations in our system:
    - NYC Area: JFK, LGA, EWR (Newark)
    - Other major cities: Check using get_all_destinations() or get_available_destinations()
    
    Special notes:
    - Many flights are recurring (daily, weekly, etc.)
    - Some routes observe religious holidays (e.g., JFK-TLV excludes Saturday for Shabbos)
    """

    user_request: str = dspy.InputField()
    process_result: str = dspy.OutputField(
        desc=(
            "A helpful response that uses your knowledge about travel, destinations, weather, and activities. "
            "When users ask for recommendations (warm, adventurous, cultural, etc.), use your general knowledge "
            "to suggest destinations, then verify availability using tools. For bookings, provide confirmation numbers."
        )
    )


# Configure DSPy with OpenAI - using gpt-4 for better reasoning
lm = dspy.LM(model='openai/gpt-4o-mini', api_key=get_openai_key())
dspy.configure(lm=lm)

# Create the ReAct agent with max_iters to prevent excessive tool calling
agent = dspy.ReAct(
    DSPyAirlineCustomerService,
    tools=[
        get_all_destinations,
        get_available_destinations,
        search_routes,
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
    # Start MLflow session run
    with mlflow.start_run(run_name="Agent_Session"):
        mlflow.log_param("model", "gpt-4o-mini")
        mlflow.log_param("agent_type", "ReAct")
        mlflow.log_param("max_iters", 5)
        
        interaction_count = 0
        
        while True:
            user_request = input("\nUser: ").strip()
            if not user_request or user_request.lower() in ['exit', 'quit', 'bye']:
                print("Thank you for using our service. Goodbye!")
                break
            
            interaction_count += 1
            
            # Create a nested run for each interaction to capture separate traces
            with mlflow.start_run(run_name=f"Interaction_{interaction_count}", nested=True):
                # Log user request
                mlflow.log_param("user_request", user_request[:100])
                mlflow.log_text(user_request, f"request_{interaction_count}.txt")
                
                result = agent(user_request=user_request)
                print(f"Agent: {result.process_result}")
                
                # Log response
                mlflow.log_text(result.process_result, f"response_{interaction_count}.txt")
            
            # Log to parent run
            mlflow.log_metric("total_interactions", interaction_count, step=interaction_count)
            
            # Log to parent run
            mlflow.log_metric("total_interactions", interaction_count, step=interaction_count)
    # Test case: Book a flight
    

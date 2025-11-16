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

# Set up MLflow tracking
mlflow.set_experiment("dspy_airline_agent")


class DSPyAirlineCustomerService(dspy.Signature):
    """You are an airline customer service agent that helps user book and manage flights.

    You are given a list of tools to handle user request, and you should decide the right tool to use in order to
    fulfill users' request."""

    user_request: str = dspy.InputField()
    process_result: str = dspy.OutputField(
        desc=(
            "Message that summarizes the process result, and the information users need, e.g., the "
            "confirmation_number if a new flight is booked."
        )
    )


# Configure DSPy with OpenAI
lm = dspy.OpenAI(model='gpt-3.5-turbo', api_key=get_openai_key())
dspy.settings.configure(lm=lm)

# Create the ReAct agent
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
    ]
)


if __name__ == "__main__":
    # Example usage
    print("=== DSPy Airline Customer Service Agent ===\n")
    
    # Start MLflow run
    with mlflow.start_run():
        mlflow.log_param("model", "gpt-3.5-turbo")
        mlflow.log_param("agent_type", "ReAct")
        
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
    

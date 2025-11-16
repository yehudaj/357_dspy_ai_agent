"""AI Agent for airline customer service using DSPy."""
import dspy
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
    while True:
        user_request = input("\nUser: ").strip()
        if not user_request or user_request.lower() in ['exit', 'quit', 'bye']:
            print("Thank you for using our service. Goodbye!")
            break
        
        result = agent(user_request=user_request)
        print(f"Agent: {result.process_result}")
    # Test case: Book a flight
    

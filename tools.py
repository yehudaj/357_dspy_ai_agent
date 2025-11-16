"""Tools for the DSPy AI agent to interact with flight booking system."""
import random
import string
from datetime import datetime
from typing import Optional
from datamodel import (
    Date,
    Flight,
    UserProfile,
    Itinerary,
    Ticket,
    flight_database,
    itinerary_database,
    ticket_database,
    user_database,
)


def get_available_destinations(origin: str):
    """Get all available destinations from a given origin airport.
    
    Args:
        origin: Airport code (e.g., 'JFK', 'LGA', 'EWR')
    
    Returns:
        List of destination airport codes available from this origin
    """
    destinations = set()
    for flight in flight_database.values():
        if flight.origin == origin:
            destinations.add(flight.destination)
    return sorted(list(destinations))


def get_all_destinations():
    """Get all available destination airports in the system.
    
    Returns:
        List of all destination airport codes
    """
    destinations = set()
    for flight in flight_database.values():
        destinations.add(flight.destination)
    return sorted(list(destinations))


def search_routes(origin: str, destination: Optional[str] = None):
    """Search for available routes from an origin, optionally filtered by destination.
    
    Args:
        origin: Origin airport code
        destination: Optional destination airport code to filter by
    
    Returns:
        List of flight information including route, schedule, and pricing
    """
    routes = []
    for flight in flight_database.values():
        if flight.origin == origin:
            if destination is None or flight.destination == destination:
                route_info = {
                    "flight_id": flight.flight_id,
                    "route": f"{flight.origin} -> {flight.destination}",
                    "duration": flight.duration,
                    "price": flight.price,
                    "sample_time": f"{flight.date_time.hour}:00",
                    "recurring": flight.recurring_schedule is not None,
                }
                if flight.recurring_schedule:
                    route_info["frequency"] = flight.recurring_schedule.frequency
                    if flight.recurring_schedule.excluded_days:
                        route_info["excluded_days"] = [day.value for day in flight.recurring_schedule.excluded_days]
                routes.append(route_info)
    return routes


def fetch_flight_info(date: Date, origin: str, destination: str):
    """Fetch flight information from origin to destination on the given date"""
    flights = []

    for flight_id, flight in flight_database.items():
        if (
            flight.date_time.year == date.year
            and flight.date_time.month == date.month
            and flight.date_time.day == date.day
            and flight.origin == origin
            and flight.destination == destination
        ):
            flights.append(flight)
    if len(flights) == 0:
        raise ValueError("No matching flight found!")
    return flights


def fetch_itinerary(confirmation_number: str):
    """Fetch a booked itinerary information from database"""
    return itinerary_database.get(confirmation_number)


def pick_flight(flights: list[Flight]):
    """Pick up the best flight that matches users' request. we pick the shortest, and cheaper one on ties."""
    sorted_flights = sorted(
        flights,
        key=lambda x: (
            x.get("duration") if isinstance(x, dict) else x.duration,
            x.get("price") if isinstance(x, dict) else x.price,
        ),
    )
    return sorted_flights[0]


def _generate_id(length=8):
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choices(chars, k=length))


def book_flight(flight: Flight, user_profile: UserProfile):
    """Book a flight on behalf of the user."""
    confirmation_number = _generate_id()
    while confirmation_number in itinerary_database:
        confirmation_number = _generate_id()
    itinerary_database[confirmation_number] = Itinerary(
        confirmation_number=confirmation_number,
        user_profile=user_profile,
        flight=flight,
    )
    return confirmation_number, itinerary_database[confirmation_number]


def cancel_itinerary(confirmation_number: str, user_profile: UserProfile):
    """Cancel an itinerary on behalf of the user."""
    if confirmation_number in itinerary_database:
        del itinerary_database[confirmation_number]
        return
    raise ValueError("Cannot find the itinerary, please check your confirmation number.")


def get_user_info(name: str):
    """Fetch the user profile from database with given name."""
    return user_database.get(name)


def file_ticket(user_request: str, user_profile: UserProfile):
    """File a customer support ticket if this is something the agent cannot handle."""
    ticket_id = _generate_id(length=6)
    ticket_database[ticket_id] = Ticket(
        user_request=user_request,
        user_profile=user_profile,
    )
    return ticket_id

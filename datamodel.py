"""Data models for the AI agent."""
from pydantic import BaseModel
from typing import Optional, Literal
from enum import Enum


class DayOfWeek(str, Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"


class Date(BaseModel):
    # Somehow LLM is bad at specifying `datetime.datetime`, so
    # we define a custom class to represent the date.
    year: int
    month: int
    day: int
    hour: int


class RecurringSchedule(BaseModel):
    """Schedule for recurring flights"""
    frequency: Literal["daily", "weekly", "weekdays", "weekends"]
    excluded_days: list[DayOfWeek] = []  # e.g., exclude Saturday for Shabbos
    days_of_week: Optional[list[DayOfWeek]] = None  # for weekly frequency


class UserProfile(BaseModel):
    user_id: str
    name: str
    email: str


class Flight(BaseModel):
    flight_id: str
    date_time: Date
    origin: str
    destination: str
    duration: float
    price: float
    recurring_schedule: Optional[RecurringSchedule] = None  # None means one-time flight


class Itinerary(BaseModel):
    confirmation_number: str
    user_profile: UserProfile
    flight: Flight


class Ticket(BaseModel):
    user_request: str
    user_profile: UserProfile


# Database with dummy data
user_database = {
    "Adam": UserProfile(user_id="1", name="Adam", email="adam@gmail.com"),
    "Bob": UserProfile(user_id="2", name="Bob", email="bob@gmail.com"),
    "Chelsie": UserProfile(user_id="3", name="Chelsie", email="chelsie@gmail.com"),
    "David": UserProfile(user_id="4", name="David", email="david@gmail.com"),
    "Emma": UserProfile(user_id="5", name="Emma", email="emma@gmail.com"),
    "Frank": UserProfile(user_id="6", name="Frank", email="frank@gmail.com"),
    "Grace": UserProfile(user_id="7", name="Grace", email="grace@gmail.com"),
    "Henry": UserProfile(user_id="8", name="Henry", email="henry@gmail.com"),
}

flight_database = {
    # JFK to TLV (New York JFK to Tel Aviv) - Daily except Saturday (Shabbos)
    "DA1001": Flight(
        flight_id="DA1001",
        origin="JFK",
        destination="TLV",
        date_time=Date(year=2025, month=12, day=1, hour=23),
        duration=11.0,
        price=850,
        recurring_schedule=RecurringSchedule(
            frequency="daily",
            excluded_days=[DayOfWeek.SATURDAY]
        )
    ),
    "DA1002": Flight(
        flight_id="DA1002",
        origin="JFK",
        destination="TLV",
        date_time=Date(year=2025, month=12, day=1, hour=10),
        duration=11.0,
        price=920,
        recurring_schedule=RecurringSchedule(
            frequency="daily",
            excluded_days=[DayOfWeek.SATURDAY]
        )
    ),
    
    # JFK to MIA (New York to Miami) - Daily warm destination
    "DA1010": Flight(
        flight_id="DA1010",
        origin="JFK",
        destination="MIA",
        date_time=Date(year=2025, month=12, day=1, hour=7),
        duration=3.0,
        price=280,
        recurring_schedule=RecurringSchedule(frequency="daily", excluded_days=[])
    ),
    "DA1011": Flight(
        flight_id="DA1011",
        origin="JFK",
        destination="MIA",
        date_time=Date(year=2025, month=12, day=1, hour=14),
        duration=3.0,
        price=310,
        recurring_schedule=RecurringSchedule(frequency="daily", excluded_days=[])
    ),
    
    # LGA to MIA (LaGuardia to Miami) - Weekdays
    "DA1020": Flight(
        flight_id="DA1020",
        origin="LGA",
        destination="MIA",
        date_time=Date(year=2025, month=12, day=2, hour=8),
        duration=3.0,
        price=260,
        recurring_schedule=RecurringSchedule(frequency="weekdays", excluded_days=[])
    ),
    
    # EWR to MIA (Newark to Miami) - Daily
    "DA1030": Flight(
        flight_id="DA1030",
        origin="EWR",
        destination="MIA",
        date_time=Date(year=2025, month=12, day=1, hour=9),
        duration=3.0,
        price=270,
        recurring_schedule=RecurringSchedule(frequency="daily", excluded_days=[])
    ),
    
    # JFK to LAX (New York to Los Angeles) - Daily
    "DA1040": Flight(
        flight_id="DA1040",
        origin="JFK",
        destination="LAX",
        date_time=Date(year=2025, month=12, day=1, hour=6),
        duration=6.0,
        price=420,
        recurring_schedule=RecurringSchedule(frequency="daily", excluded_days=[])
    ),
    "DA1041": Flight(
        flight_id="DA1041",
        origin="JFK",
        destination="LAX",
        date_time=Date(year=2025, month=12, day=1, hour=13),
        duration=6.0,
        price=450,
        recurring_schedule=RecurringSchedule(frequency="daily", excluded_days=[])
    ),
    
    # LGA to FLL (LaGuardia to Fort Lauderdale) - Daily warm destination
    "DA1050": Flight(
        flight_id="DA1050",
        origin="LGA",
        destination="FLL",
        date_time=Date(year=2025, month=12, day=1, hour=7),
        duration=3.0,
        price=240,
        recurring_schedule=RecurringSchedule(frequency="daily", excluded_days=[])
    ),
    
    # EWR to MCO (Newark to Orlando) - Daily warm destination
    "DA1060": Flight(
        flight_id="DA1060",
        origin="EWR",
        destination="MCO",
        date_time=Date(year=2025, month=12, day=1, hour=8),
        duration=2.5,
        price=220,
        recurring_schedule=RecurringSchedule(frequency="daily", excluded_days=[])
    ),
    
    # JFK to SAN (New York to San Diego) - Every Tuesday and Thursday
    "DA1070": Flight(
        flight_id="DA1070",
        origin="JFK",
        destination="SAN",
        date_time=Date(year=2025, month=12, day=2, hour=9),
        duration=6.0,
        price=480,
        recurring_schedule=RecurringSchedule(
            frequency="weekly",
            days_of_week=[DayOfWeek.TUESDAY, DayOfWeek.THURSDAY],
            excluded_days=[]
        )
    ),
    
    # TLV to JFK (Tel Aviv to New York) - Daily except Saturday
    "DA1080": Flight(
        flight_id="DA1080",
        origin="TLV",
        destination="JFK",
        date_time=Date(year=2025, month=12, day=1, hour=14),
        duration=12.0,
        price=880,
        recurring_schedule=RecurringSchedule(
            frequency="daily",
            excluded_days=[DayOfWeek.SATURDAY]
        )
    ),
    
    # EWR to TLV (Newark to Tel Aviv) - Sunday, Tuesday, Thursday
    "DA1090": Flight(
        flight_id="DA1090",
        origin="EWR",
        destination="TLV",
        date_time=Date(year=2025, month=12, day=1, hour=22),
        duration=11.0,
        price=830,
        recurring_schedule=RecurringSchedule(
            frequency="weekly",
            days_of_week=[DayOfWeek.SUNDAY, DayOfWeek.TUESDAY, DayOfWeek.THURSDAY],
            excluded_days=[]
        )
    ),
    
    # SFO to JFK (San Francisco to New York)
    "DA123": Flight(
        flight_id="DA123",
        origin="SFO",
        destination="JFK",
        date_time=Date(year=2025, month=9, day=1, hour=1),
        duration=5.5,
        price=320,
    ),
    "DA125": Flight(
        flight_id="DA125",
        origin="SFO",
        destination="JFK",
        date_time=Date(year=2025, month=9, day=1, hour=7),
        duration=5.5,
        price=450,
    ),
    "DA127": Flight(
        flight_id="DA127",
        origin="SFO",
        destination="JFK",
        date_time=Date(year=2025, month=9, day=1, hour=14),
        duration=6.0,
        price=380,
    ),
    
    # SFO to SNA (San Francisco to Orange County)
    "DA456": Flight(
        flight_id="DA456",
        origin="SFO",
        destination="SNA",
        date_time=Date(year=2025, month=10, day=1, hour=1),
        duration=1.5,
        price=150,
    ),
    "DA460": Flight(
        flight_id="DA460",
        origin="SFO",
        destination="SNA",
        date_time=Date(year=2025, month=10, day=1, hour=9),
        duration=1.5,
        price=180,
    ),
    
    # SFO to LAX (San Francisco to Los Angeles)
    "DA200": Flight(
        flight_id="DA200",
        origin="SFO",
        destination="LAX",
        date_time=Date(year=2025, month=9, day=15, hour=6),
        duration=1.5,
        price=120,
    ),
    "DA202": Flight(
        flight_id="DA202",
        origin="SFO",
        destination="LAX",
        date_time=Date(year=2025, month=9, day=15, hour=12),
        duration=1.5,
        price=140,
    ),
    "DA204": Flight(
        flight_id="DA204",
        origin="SFO",
        destination="LAX",
        date_time=Date(year=2025, month=9, day=15, hour=18),
        duration=1.5,
        price=160,
    ),
    
    # LAX to JFK (Los Angeles to New York)
    "DA300": Flight(
        flight_id="DA300",
        origin="LAX",
        destination="JFK",
        date_time=Date(year=2025, month=9, day=20, hour=8),
        duration=5.0,
        price=350,
    ),
    "DA302": Flight(
        flight_id="DA302",
        origin="LAX",
        destination="JFK",
        date_time=Date(year=2025, month=9, day=20, hour=13),
        duration=5.5,
        price=420,
    ),
    
    # JFK to ORD (New York to Chicago)
    "DA400": Flight(
        flight_id="DA400",
        origin="JFK",
        destination="ORD",
        date_time=Date(year=2025, month=10, day=5, hour=7),
        duration=2.5,
        price=220,
    ),
    "DA402": Flight(
        flight_id="DA402",
        origin="JFK",
        destination="ORD",
        date_time=Date(year=2025, month=10, day=5, hour=15),
        duration=2.5,
        price=250,
    ),
    
    # ORD to SFO (Chicago to San Francisco)
    "DA500": Flight(
        flight_id="DA500",
        origin="ORD",
        destination="SFO",
        date_time=Date(year=2025, month=11, day=1, hour=9),
        duration=4.5,
        price=380,
    ),
    "DA502": Flight(
        flight_id="DA502",
        origin="ORD",
        destination="SFO",
        date_time=Date(year=2025, month=11, day=1, hour=16),
        duration=4.5,
        price=410,
    ),
    
    # SEA to LAX (Seattle to Los Angeles)
    "DA600": Flight(
        flight_id="DA600",
        origin="SEA",
        destination="LAX",
        date_time=Date(year=2025, month=9, day=10, hour=6),
        duration=2.5,
        price=180,
    ),
    "DA602": Flight(
        flight_id="DA602",
        origin="SEA",
        destination="LAX",
        date_time=Date(year=2025, month=9, day=10, hour=14),
        duration=2.5,
        price=200,
    ),
    
    # MIA to JFK (Miami to New York)
    "DA700": Flight(
        flight_id="DA700",
        origin="MIA",
        destination="JFK",
        date_time=Date(year=2025, month=10, day=15, hour=8),
        duration=3.0,
        price=280,
    ),
    "DA702": Flight(
        flight_id="DA702",
        origin="MIA",
        destination="JFK",
        date_time=Date(year=2025, month=10, day=15, hour=17),
        duration=3.0,
        price=310,
    ),
    
    # BOS to SFO (Boston to San Francisco)
    "DA800": Flight(
        flight_id="DA800",
        origin="BOS",
        destination="SFO",
        date_time=Date(year=2025, month=11, day=10, hour=7),
        duration=6.0,
        price=450,
    ),
    "DA802": Flight(
        flight_id="DA802",
        origin="BOS",
        destination="SFO",
        date_time=Date(year=2025, month=11, day=10, hour=13),
        duration=6.0,
        price=480,
    ),
    
    # DEN to ORD (Denver to Chicago)
    "DA900": Flight(
        flight_id="DA900",
        origin="DEN",
        destination="ORD",
        date_time=Date(year=2025, month=9, day=25, hour=10),
        duration=2.5,
        price=190,
    ),
    "DA902": Flight(
        flight_id="DA902",
        origin="DEN",
        destination="ORD",
        date_time=Date(year=2025, month=9, day=25, hour=16),
        duration=2.5,
        price=210,
    ),
}

itinerary_database = {}
ticket_database = {}

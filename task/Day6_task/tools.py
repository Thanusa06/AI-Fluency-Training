# tools.py

"""
Tools for the Weekend Trip Assistant.

Scenario:
A user wants help planning a short trip.
The agent can:
1. Check weather information for a city.
2. Calculate a simple trip budget.

The SCHEMAS dictionary is used both:
- when sending tool definitions to the model
- when validating arguments before execution
"""


# ---------------------------------------------------------
# TOOL 1: WEATHER
# ---------------------------------------------------------

WEATHER_DATA = {
    "Chennai": {
        "temperature": 30,
        "condition": "Sunny"
    },
    "Bengaluru": {
        "temperature": 24,
        "condition": "Cloudy"
    },
    "Ooty": {
        "temperature": 18,
        "condition": "Cool"
    },
    "Coimbatore": {
        "temperature": 27,
        "condition": "Partly Cloudy"
    }
}


def get_weather(city: str, unit: str) -> str:
    """
    Return simple weather information for a city.
    """

    data = WEATHER_DATA.get(city)

    if data is None:
        return f"Weather data is not available for {city}."

    temperature = data["temperature"]

    if unit == "F":
        temperature = round((temperature * 9 / 5) + 32, 1)

    return (
        f"Weather in {city}: "
        f"{temperature}°{unit}, "
        f"{data['condition']}."
    )


# ---------------------------------------------------------
# TOOL 2: BUDGET CALCULATOR
# ---------------------------------------------------------


def calculate_budget(
    transport: float,
    accommodation_per_day: float,
    food_per_day: float,
    days: int,
    currency: str
) -> str:
    """
    Calculate the total trip budget.
    """

    transport_cost = transport
    accommodation_cost = accommodation_per_day * days
    food_cost = food_per_day * days

    total = (
        transport_cost
        + accommodation_cost
        + food_cost
    )

    return (
        f"Trip budget for {days} day(s): "
        f"Transport={currency}{transport_cost:.2f}, "
        f"Accommodation={currency}{accommodation_cost:.2f}, "
        f"Food={currency}{food_cost:.2f}, "
        f"Total={currency}{total:.2f}."
    )


# ---------------------------------------------------------
# SINGLE SOURCE OF TRUTH FOR TOOL SCHEMAS
# ---------------------------------------------------------

SCHEMAS = {

    "get_weather": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "Name of the destination city."
            },
            "unit": {
                "type": "string",
                "description": "Temperature unit.",
                "enum": ["C", "F"]
            }
        },
        "required": [
            "city",
            "unit"
        ],
        "additionalProperties": False
    },

    "calculate_budget": {
        "type": "object",
        "properties": {
            "transport": {
                "type": "number",
                "description": "Transport cost for the trip."
            },
            "accommodation_per_day": {
                "type": "number",
                "description": "Accommodation cost per day."
            },
            "food_per_day": {
                "type": "number",
                "description": "Food cost per day."
            },
            "days": {
                "type": "integer",
                "description": "Number of trip days."
            },
            "currency": {
                "type": "string",
                "description": "Currency symbol.",
                "enum": ["Rs", "USD"]
            }
        },
        "required": [
            "transport",
            "accommodation_per_day",
            "food_per_day",
            "days",
            "currency"
        ],
        "additionalProperties": False
    }
}


# ---------------------------------------------------------
# MAP TOOL NAMES TO ACTUAL PYTHON FUNCTIONS
# ---------------------------------------------------------

TOOLS = {
    "get_weather": get_weather,
    "calculate_budget": calculate_budget
}


# ---------------------------------------------------------
# CONVERT OUR SCHEMAS INTO OPENAI TOOL DEFINITIONS
# ---------------------------------------------------------

TOOL_DEFINITIONS = []

for name, schema in SCHEMAS.items():

    description = {
        "get_weather":
            "Get weather information for a destination city.",

        "calculate_budget":
            "Calculate the total cost of a trip."
    }[name]

    TOOL_DEFINITIONS.append({
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": schema
        }
    })
    
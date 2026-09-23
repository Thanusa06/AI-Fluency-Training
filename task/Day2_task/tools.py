import requests


def get_chennai_weather():
    """Get current weather information for Chennai using Open-Meteo."""
    
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=13.0827"
        "&longitude=80.2707"
        "&current=temperature_2m,weather_code"
    )

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    temperature = data["current"]["temperature_2m"]
    weather_code = data["current"]["weather_code"]

    return {
        "temperature": temperature,
        "weather_code": weather_code
    }


def weather_description(code):
    descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Foggy",
        51: "Light drizzle",
        61: "Rain",
        63: "Moderate rain",
        80: "Rain showers",
        95: "Thunderstorm"
    }

    return descriptions.get(code, "Unknown weather condition")
import os
from openai import OpenAI
from tools import get_chennai_weather, weather_description

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def react_agent():
    question = """
Plan a weekend trip to Chennai.

I have a budget of ₹5000.
Travel costs ₹1500 and accommodation costs ₹1200.

Tell me:
1. How much money remains after travel and accommodation?
2. What is the current weather in Chennai?

For the current weather, use the available weather tool.
"""

    print("\n--- ReACT AGENT ---")
    print("Question:", question)

    print("\nThought: I need to calculate the budget and obtain current weather.")

    remaining = 5000 - 1500 - 1200

    print("Action: Calling the Chennai weather tool...")

    try:
        weather = get_chennai_weather()

        description = weather_description(weather["weather_code"])
        temperature = weather["temperature"]

        print(
            f"Observation: Chennai temperature is "
            f"{temperature}°C and the condition is {description}."
        )

        print("\nFinal Answer:")
        print(f"Remaining budget: ₹{remaining}")
        print(f"Current Chennai weather: {temperature}°C, {description}")

    except Exception as e:
        print("\nTool error:", e)
        print(f"Remaining budget: ₹{remaining}")
        print("Weather information could not be retrieved.")


if __name__ == "__main__":
    react_agent()
    
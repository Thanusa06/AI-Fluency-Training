import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def chain_of_thought():
    question = """
You are helping plan a weekend trip.

A person has a total budget of ₹5000.
Travel costs ₹1500.
Accommodation costs ₹1200.
Food costs ₹800.
They also want to buy souvenirs costing ₹500.

Calculate how much money remains after all expenses.

Work through the calculation carefully and give the final answer.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0.7
    )

    print("\n--- CHAIN-OF-THOUGHT ---")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    chain_of_thought()
    
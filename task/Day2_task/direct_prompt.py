import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def direct_prompt():
    question = """
You are helping plan a weekend trip to Chennai.

Answer these questions:
1. If the total budget is ₹5000, travel costs ₹1500, and accommodation costs ₹1200,
   how much money remains?
2. If I visit 3 places on Saturday and 2 places on Sunday,
   how many places will I visit in total?

Give the final answers clearly.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0
    )

    print("\n--- DIRECT PROMPTING ---")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    direct_prompt()
    
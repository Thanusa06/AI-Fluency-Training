import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def ask_question(temperature):
    question = """
A person has ₹5000 for a weekend trip.

They spend:
- ₹1500 on travel
- ₹1200 on accommodation
- ₹800 on food
- ₹500 on souvenirs

How much money remains?
Give only the final amount.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=temperature
    )

    return response.choices[0].message.content.strip()


def run_self_consistency():
    print("\n--- SELF-CONSISTENCY EXPERIMENT ---")
    print("Temperature: 0.7")
    print()

    answers = []

    for i in range(5):
        answer = ask_question(0.7)
        answers.append(answer)
        print(f"Run {i + 1}: {answer}")

    print("\n--- TEMPERATURE 0 ---")
    
    for i in range(3):
        answer = ask_question(0)
        print(f"Run {i + 1}: {answer}")


if __name__ == "__main__":
    run_self_consistency()
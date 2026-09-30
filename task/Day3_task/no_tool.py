from config import client, MODEL


QUESTIONS = [
    "What are some effective ways to improve in mathematics?",
    "What is Arun's Maths mark?",
    "Why is it useful to track your subject marks?"
]


for question in QUESTIONS:
    print("\n" + "=" * 60)
    print("QUESTION:", question)
    print("=" * 60)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful student assistant. "
                    "Answer the user's question clearly. "
                    "Do not claim access to private student data unless it is provided."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    answer = response.choices[0].message.content

    print("ANSWER:", answer)

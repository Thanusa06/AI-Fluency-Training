import os
import time

from openai import OpenAI


def load_simple_env():

    with open(".env", "r", encoding="utf-8") as file:

        for line in file:

            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" in line:

                key, value = line.split("=", 1)

                os.environ[key.strip()] = value.strip()


load_simple_env()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")


if not GROQ_API_KEY:

    raise ValueError(
        "GROQ_API_KEY is missing from .env"
    )


client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


MODELS = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b"
]


PROMPTS = [

    "Reply with exactly: OK",

    "In two sentences, what is an AI agent?",

    """
A course costs Rs. 18,000 with a 15% scholarship.
What is payable? Show the steps.
"""
]


def run_model(model, prompt):

    start = time.perf_counter()

    response = client.chat.completions.create(

        model=model,

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0
    )

    end = time.perf_counter()

    elapsed = end - start

    answer = response.choices[0].message.content

    completion_tokens = 0

    if response.usage:

        completion_tokens = (
            response.usage.completion_tokens
        )

    if elapsed > 0:

        tokens_per_second = (
            completion_tokens / elapsed
        )

    else:

        tokens_per_second = 0

    return {
        "elapsed": elapsed,
        "completion_tokens": completion_tokens,
        "tokens_per_second": tokens_per_second,
        "answer": answer
    }


def main():

    print("=" * 60)
    print("DAY 5 - GROQ MODEL BENCHMARK")
    print("=" * 60)

    for model in MODELS:

        print("\n")
        print("=" * 60)
        print("MODEL:", model)
        print("=" * 60)

        for number, prompt in enumerate(
            PROMPTS,
            start=1
        ):

            print(
                f"\n--- Prompt {number} ---"
            )

            print(prompt.strip())

            try:

                result = run_model(
                    model,
                    prompt
                )

                print("\nAnswer:")

                print(
                    result["answer"]
                )

                print(
                    "\nElapsed:",
                    round(
                        result["elapsed"],
                        3
                    ),
                    "seconds"
                )

                print(
                    "Completion tokens:",
                    result["completion_tokens"]
                )

                print(
                    "Approx tokens/sec:",
                    round(
                        result["tokens_per_second"],
                        2
                    )
                )

            except Exception as error:

                print("\nRequest failed:")

                print(error)


if __name__ == "__main__":

    main()
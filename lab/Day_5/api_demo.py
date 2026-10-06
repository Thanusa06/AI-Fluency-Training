import os
import time

from openai import OpenAI


# --------------------------------------------------
# Load .env without python-dotenv
# --------------------------------------------------

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


# --------------------------------------------------
# Read configuration
# --------------------------------------------------

PROVIDER = os.getenv(
    "PROVIDER",
    "groq"
).strip().lower()

MODEL = os.getenv(
    "MODEL",
    "openai/gpt-oss-120b"
)

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)


# --------------------------------------------------
# Check configuration
# --------------------------------------------------

if PROVIDER != "groq":

    raise ValueError(
        "This Day 5 project is configured to use Groq."
    )


if not GROQ_API_KEY:

    raise ValueError(
        "GROQ_API_KEY is missing from .env"
    )


# --------------------------------------------------
# Create Groq client
# --------------------------------------------------

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


PROMPT = (
    "In three sentences, explain what an AI agent is."
)


# --------------------------------------------------
# Part 1: Normal API request
# --------------------------------------------------

def normal_completion():

    print("\n" + "=" * 60)
    print("1. NORMAL COMPLETION")
    print("=" * 60)

    start = time.perf_counter()

    response = client.chat.completions.create(

        model=MODEL,

        messages=[
            {
                "role": "user",
                "content": PROMPT
            }
        ],

        temperature=0
    )

    end = time.perf_counter()

    elapsed = end - start

    answer = response.choices[0].message.content

    print("\nAnswer:")
    print(answer)

    print("\nModel:", MODEL)

    print(
        "Elapsed time:",
        round(elapsed, 3),
        "seconds"
    )

    if response.usage:

        print(
            "Prompt tokens:",
            response.usage.prompt_tokens
        )

        print(
            "Completion tokens:",
            response.usage.completion_tokens
        )

        print(
            "Total tokens:",
            response.usage.total_tokens
        )

        if elapsed > 0:

            tokens_per_second = (
                response.usage.completion_tokens
                / elapsed
            )

            print(
                "Approx tokens/sec:",
                round(tokens_per_second, 2)
            )


# --------------------------------------------------
# Part 2: Streaming + TTFT
# --------------------------------------------------

def streaming_completion():

    print("\n" + "=" * 60)
    print("2. STREAMING + TTFT")
    print("=" * 60)

    start = time.perf_counter()

    first_token_time = None

    stream = client.chat.completions.create(

        model=MODEL,

        messages=[
            {
                "role": "user",
                "content": PROMPT
            }
        ],

        temperature=0,

        stream=True
    )

    print("\nAnswer:")

    for chunk in stream:

        if not chunk.choices:
            continue

        content = chunk.choices[0].delta.content

        if content:

            if first_token_time is None:

                first_token_time = time.perf_counter()

            print(
                content,
                end="",
                flush=True
            )

    end = time.perf_counter()

    print()

    if first_token_time is not None:

        ttft = (
            first_token_time - start
        )

        print(
            "TTFT:",
            round(ttft, 3),
            "seconds"
        )

    print(
        "Total time:",
        round(end - start, 3),
        "seconds"
    )


# --------------------------------------------------
# Part 3: System prompt
# --------------------------------------------------

def system_prompt_test():

    print("\n" + "=" * 60)
    print("3. SYSTEM PROMPT TEST")
    print("=" * 60)

    response = client.chat.completions.create(

        model=MODEL,

        messages=[
            {
                "role": "system",
                "content": (
                    "You are a college fee assistant. "
                    "Never guess fees. "
                    "Keep answers short."
                )
            },

            {
                "role": "user",
                "content": (
                    "A course costs Rs. 18,000. "
                    "What is the fee?"
                )
            }
        ],

        temperature=0
    )

    print("\nSystem prompt:")

    print(
        "You are a college fee assistant. "
        "Never guess fees. Keep answers short."
    )

    print("\nAnswer:")

    print(
        response.choices[0].message.content
    )


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("=" * 60)
    print("DAY 5 - GROQ MODEL SERVING DEMO")
    print("=" * 60)

    print("Provider:", PROVIDER)

    print("Model:", MODEL)

    normal_completion()

    streaming_completion()

    system_prompt_test()


if __name__ == "__main__":

    main()
    
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


PROVIDER = os.getenv(
    "PROVIDER",
    "ollama"
).strip().lower()

MODEL = os.getenv(
    "MODEL",
    "qwen2.5:1.5b"
).strip()


print("=" * 60)
print("DAY 6 SETUP CHECK")
print("=" * 60)

print("Provider:", PROVIDER)
print("Model:", MODEL)


# Check provider configuration
if PROVIDER == "ollama":

    base_url = "http://localhost:11434/v1"
    api_key = "ollama"

elif PROVIDER == "groq":

    base_url = "https://api.groq.com/openai/v1"
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        print()
        print("ERROR: GROQ_API_KEY is missing from .env")
        print()
        print("Add:")
        print("GROQ_API_KEY=your_groq_api_key")
        raise SystemExit(1)

elif PROVIDER == "huggingface":

    base_url = "https://router.huggingface.co/v1"
    api_key = os.getenv("HF_TOKEN")

    if not api_key:
        print()
        print("ERROR: HF_TOKEN is missing from .env")
        raise SystemExit(1)

else:

    print()
    print("ERROR: Unknown provider:", PROVIDER)
    print("Use: ollama, groq, or huggingface")
    raise SystemExit(1)


# Create client
client = OpenAI(
    base_url=base_url,
    api_key=api_key,
)


print()
print("Trying to connect to the model...")


try:

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": "Reply with exactly: SETUP OK",
            }
        ],
        temperature=0,
        max_tokens=20,
    )

    answer = response.choices[0].message.content

    print()
    print("Model response:", answer)
    print()
    print("SETUP OK")

except Exception as error:

    print()
    print("SETUP FAILED")
    print(type(error).__name__)
    print(error)
    
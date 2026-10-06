import os

from dotenv import load_dotenv
from openai import OpenAI


# Read the .env file
load_dotenv()


# Read provider and model
PROVIDER = os.getenv("PROVIDER", "ollama").strip().lower()
MODEL = os.getenv("MODEL", "qwen2.5:1.5b").strip()


# Configure the API depending on the provider
if PROVIDER == "ollama":

    BASE_URL = "http://localhost:11434/v1"
    API_KEY = "ollama"

elif PROVIDER == "groq":

    BASE_URL = "https://api.groq.com/openai/v1"
    API_KEY = os.getenv("GROQ_API_KEY")

elif PROVIDER == "huggingface":

    BASE_URL = "https://router.huggingface.co/v1"
    API_KEY = os.getenv("HF_TOKEN")

else:

    raise ValueError(
        f"Unknown provider: {PROVIDER}. "
        "Use ollama, groq, or huggingface."
    )


# Create the OpenAI-compatible client
client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
)


def banner(title):
    """Print a simple heading."""

    print("=" * 60)
    print(title)
    print(f"provider: {PROVIDER}")
    print(f"model: {MODEL}")
    print("=" * 60)
    
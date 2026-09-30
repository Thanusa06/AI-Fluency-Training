import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROVIDER = os.getenv("PROVIDER", "groq").strip().lower()

if PROVIDER != "groq":
    raise SystemExit(f"Unsupported provider: {PROVIDER}")

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")

if not API_KEY:
    raise SystemExit("GROQ_API_KEY was not found. Check your .env file.")

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=API_KEY
)

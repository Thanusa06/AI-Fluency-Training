
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from the task folder.
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Model configuration
PROVIDER = os.getenv("PROVIDER", "groq")
MODEL = os.getenv("MODEL", "openai/gpt-oss-120b")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Embedding configuration
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "BAAI/bge-small-en-v1.5"
)

# Chroma database location
CHROMA_DB_DIR = str(BASE_DIR / "chroma_db")

# Search distance threshold.
# We will tune this using measured scores in Part C.
MAX_DISTANCE = float(os.getenv("MAX_DISTANCE", "0.8"))


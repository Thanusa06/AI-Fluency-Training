# structured_outputs.py

"""
Structured output comparison.

The same extraction question is asked three ways:

1. No constraint
2. JSON mode
3. JSON Schema mode

If the provider does not support a mode,
the error is printed instead of crashing.
"""

import json
import os

from dotenv import load_dotenv
from openai import OpenAI


# ---------------------------------------------------------
# LOAD ENVIRONMENT
# ---------------------------------------------------------

load_dotenv()

MODEL = os.getenv(
    "MODEL",
    "openai/gpt-oss-120b"
)

BASE_URL = os.getenv(
    "BASE_URL",
    "https://api.groq.com/openai/v1"
)

API_KEY = os.getenv(
    "API_KEY",
    "dummy"
)


client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)


# ---------------------------------------------------------
# EXTRACTION QUESTION
# ---------------------------------------------------------

QUESTION = """
Extract the trip information from this sentence:

"Thanusa wants to visit Ooty for 2 days with a budget of
Rs 5000."

Return these fields:
city
days
budget
currency
"""


# ---------------------------------------------------------
# SCHEMA
# ---------------------------------------------------------

TRIP_SCHEMA = {
    "type": "object",
    "properties": {
        "city": {
            "type": "string"
        },
        "days": {
            "type": "integer"
        },
        "budget": {
            "type": "number"
        },
        "currency": {
            "type": "string"
        }
    },
    "required": [
        "city",
        "days",
        "budget",
        "currency"
    ],
    "additionalProperties": False
}


# ---------------------------------------------------------
# CASE 1: NO CONSTRAINT
# ---------------------------------------------------------

def no_constraint():

    print("\n" + "=" * 70)
    print("CASE 1: NO CONSTRAINT")
    print("=" * 70)

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": QUESTION
                }
            ],
            temperature=0
        )

        raw = response.choices[0].message.content

        print("\nRAW REPLY:")
        print(raw)

        try:

            parsed = json.loads(raw)

            print("\nPARSED RESULT:")
            print(parsed)

        except json.JSONDecodeError:

            print(
                "\nParsed result: ERROR - reply was not valid JSON."
            )

    except Exception as error:

        print("\nERROR:")
        print(error)


# ---------------------------------------------------------
# CASE 2: JSON MODE
# ---------------------------------------------------------

def json_mode():

    print("\n" + "=" * 70)
    print("CASE 2: JSON MODE")
    print("=" * 70)

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Return the requested information as JSON."
                    )
                },
                {
                    "role": "user",
                    "content": QUESTION
                }
            ],
            response_format={
                "type": "json_object"
            },
            temperature=0
        )

        raw = response.choices[0].message.content

        print("\nRAW REPLY:")
        print(raw)

        try:

            parsed = json.loads(raw)

            print("\nPARSED RESULT:")
            print(parsed)

        except json.JSONDecodeError:

            print(
                "\nParsed result: ERROR - invalid JSON."
            )

    except Exception as error:

        print("\nERROR:")
        print(error)


# ---------------------------------------------------------
# CASE 3: JSON SCHEMA MODE
# ---------------------------------------------------------

def schema_mode():

    print("\n" + "=" * 70)
    print("CASE 3: SCHEMA MODE")
    print("=" * 70)

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": QUESTION
                }
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "trip_information",
                    "strict": True,
                    "schema": TRIP_SCHEMA
                }
            },
            temperature=0
        )

        raw = response.choices[0].message.content

        print("\nRAW REPLY:")
        print(raw)

        try:

            parsed = json.loads(raw)

            print("\nPARSED RESULT:")
            print(parsed)

        except json.JSONDecodeError:

            print(
                "\nParsed result: ERROR - invalid JSON."
            )

    except Exception as error:

        print("\nERROR:")
        print(
            "Schema mode may not be supported by this provider/model."
        )
        print(error)


# ---------------------------------------------------------
# RUN ALL THREE
# ---------------------------------------------------------

if __name__ == "__main__":

    no_constraint()

    json_mode()

    schema_mode()
    
# agent.py

"""
Reliable tool-calling agent for the Day 6 task.

The loop follows four stages for every tool call:

1. Parse JSON arguments
2. Look up the tool
3. Validate arguments
4. Execute the tool

Every failure becomes a string and is returned to the model.
"""

import json
import os
from collections import Counter

from dotenv import load_dotenv
from openai import OpenAI

from tools import TOOLS, TOOL_DEFINITIONS
from validator import validate_arguments


# ---------------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ---------------------------------------------------------

load_dotenv()

PROVIDER = os.getenv("PROVIDER", "groq").strip().lower()

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


# ---------------------------------------------------------
# CREATE OPENAI-COMPATIBLE CLIENT
# ---------------------------------------------------------

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)


# ---------------------------------------------------------
# SYSTEM PROMPT
# ---------------------------------------------------------

SYSTEM_PROMPT = """
You are a reliable Weekend Trip Assistant.

You can use two tools:

1. get_weather
2. calculate_budget

Use a tool when the user asks for information that requires it.

Important:
- Do not invent tool names.
- Follow the tool schemas.
- Use only the allowed enum values.
- If a tool reports an error, correct the tool call.
- You may call multiple tools when the user asks for multiple
  independent pieces of information.
- If no tool is needed, answer directly.
"""


# ---------------------------------------------------------
# CREATE A STABLE REPRESENTATION OF A TOOL CALL
# ---------------------------------------------------------

def call_signature(tool_call):
    """
    Create a string identifying the tool and its arguments.

    This is used to detect repeated identical calls.
    """

    try:
        arguments = json.loads(
            tool_call.function.arguments
        )
    except Exception:
        arguments = tool_call.function.arguments

    return (
        tool_call.function.name,
        json.dumps(
            arguments,
            sort_keys=True,
            default=str
        )
    )


# ---------------------------------------------------------
# HANDLE ONE TOOL CALL
# ---------------------------------------------------------

def handle_tool_call(tool_call):
    """
    Handle exactly one tool call.

    Every error is returned as a string.
    No exception is allowed to crash the agent loop.
    """

    tool_name = tool_call.function.name

    raw_arguments = tool_call.function.arguments

    # -----------------------------------------------------
    # STAGE 1: PARSE JSON
    # -----------------------------------------------------

    try:

        arguments = json.loads(raw_arguments)

    except json.JSONDecodeError as error:

        return (
            "Tool error: invalid JSON arguments. "
            f"Please return valid JSON. Parser message: {error}"
        )

    # -----------------------------------------------------
    # STAGE 2: LOOK UP TOOL
    # -----------------------------------------------------

    if tool_name not in TOOLS:

        return (
            f"Tool error: unknown tool '{tool_name}'. "
            f"Available tools: {list(TOOLS.keys())}."
        )

    tool_function = TOOLS[tool_name]

    # -----------------------------------------------------
    # STAGE 3: VALIDATE
    # -----------------------------------------------------

    validation_error = validate_arguments(
        tool_name,
        arguments
    )

    if validation_error is not None:

        return validation_error

    # -----------------------------------------------------
    # STAGE 4: EXECUTE
    # -----------------------------------------------------

    try:

        result = tool_function(**arguments)

        return str(result)

    except Exception as error:

        return (
            f"Tool execution error: {error}. "
            "Please correct the arguments and try again."
        )


# ---------------------------------------------------------
# ONE API REQUEST
# ---------------------------------------------------------

def request_model(messages, max_tokens):
    """
    Send one request to the OpenAI-compatible server.
    """

    return client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOL_DEFINITIONS,
        tool_choice="auto",
        parallel_tool_calls=True,
        max_tokens=max_tokens,
        temperature=0
    )


# ---------------------------------------------------------
# MAIN AGENT LOOP
# ---------------------------------------------------------

def run_agent(
    user_question,
    max_steps=8,
    initial_max_tokens=400
):

    print("\n" + "=" * 70)
    print("USER:")
    print(user_question)
    print("=" * 70)

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_question
        }
    ]

    step = 0

    max_tokens = initial_max_tokens

    seen_calls = Counter()

    while step < max_steps:

        step += 1

        print(f"\n--- STEP {step} ---")

        # -------------------------------------------------
        # CALL MODEL
        # -------------------------------------------------

        try:

            response = request_model(
                messages,
                max_tokens
            )

        except Exception as error:

            print("API ERROR:")
            print(error)

            return {
                "steps": step,
                "answer": f"API error: {error}",
                "tool_calls": [],
                "parallel": False,
                "finish_reason": None
            }

        choice = response.choices[0]

        message = choice.message

        finish_reason = choice.finish_reason

        print("finish_reason:", finish_reason)

        # -------------------------------------------------
        # HANDLE TRUNCATED RESPONSE
        # -------------------------------------------------

        if finish_reason == "length":

            print(
                "The model response was truncated. "
                "Retrying with more tokens."
            )

            max_tokens = max_tokens * 2

            messages.append({
                "role": "assistant",
                "content": message.content or ""
            })

            continue

        # -------------------------------------------------
        # NO TOOL CALL
        # -------------------------------------------------

        if not message.tool_calls:

            answer = message.content or ""

            print("\nFINAL ANSWER:")
            print(answer)

            return {
                "steps": step,
                "answer": answer,
                "tool_calls": [],
                "parallel": False,
                "finish_reason": finish_reason
            }

        # -------------------------------------------------
        # TOOL CALLS FOUND
        # -------------------------------------------------

        tool_calls = message.tool_calls

        print(
            f"Model requested {len(tool_calls)} tool call(s)."
        )

        if len(tool_calls) > 1:

            print("PARALLEL TOOL CALLS DETECTED.")

        # -------------------------------------------------
        # ADD ASSISTANT TOOL-CALL MESSAGE
        # -------------------------------------------------

        messages.append(message)

        # -------------------------------------------------
        # PROCESS EVERY TOOL CALL
        # -------------------------------------------------

        for tool_call in tool_calls:

            signature = call_signature(tool_call)

            seen_calls[signature] += 1

            print(
                "\nTool:",
                tool_call.function.name
            )

            print(
                "Arguments:",
                tool_call.function.arguments
            )

            # -------------------------------------------------
            # REPEATED IDENTICAL CALL PROTECTION
            # -------------------------------------------------

            if seen_calls[signature] >= 3:

                result = (
                    "Tool error: the same tool call was repeated "
                    "multiple times. Stop repeating it and "
                    "try a different action."
                )

                print("REPEATED CALL BLOCKED:")

            else:

                result = handle_tool_call(
                    tool_call
                )

            print("Tool result:")
            print(result)

            # -------------------------------------------------
            # RETURN RESULT USING THE SAME tool_call_id
            # -------------------------------------------------

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

    # -----------------------------------------------------
    # MAXIMUM STEP LIMIT
    # -----------------------------------------------------

    answer = (
        "The agent stopped because the maximum number "
        "of steps was reached."
    )

    print("\nFINAL ANSWER:")
    print(answer)

    return {
        "steps": step,
        "answer": answer,
        "tool_calls": [],
        "parallel": False,
        "finish_reason": "max_steps"
    }


# ---------------------------------------------------------
# DEMO QUESTIONS
# ---------------------------------------------------------

if __name__ == "__main__":

    questions = [

        # Single tool
        "What is the weather in Chennai?",

        # Two independent tools
        (
            "What is the weather in Chennai and calculate "
            "the budget for a 2 day trip with transport "
            "Rs 1500, accommodation Rs 1200 per day and "
            "food Rs 500 per day?"
        ),

        # Tempts an invalid enum
        (
            "Tell me the weather in Ooty in Kelvin."
        ),

        # No tool
        (
            "What are three simple tips for planning "
            "a weekend trip?"
        )
    ]

    for question in questions:

        run_agent(question)
        

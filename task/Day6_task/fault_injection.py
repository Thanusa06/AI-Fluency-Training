# fault_injection.py

"""
Fault injection tests.

These tests deliberately create broken tool calls
without using a model or internet connection.

This proves that the tool handler can safely deal
with bad input.
"""

import json
from types import SimpleNamespace

from agent import handle_tool_call


def make_tool_call(tool_name, arguments):

    return SimpleNamespace(
        id="fault-test-id",
        function=SimpleNamespace(
            name=tool_name,
            arguments=arguments
        )
    )


def run_fault_test(number, name, tool_call):

    print("\n" + "=" * 70)

    print(f"FAULT {number}: {name}")

    print("=" * 70)

    result = handle_tool_call(tool_call)

    print("Returned message:")
    print(result)

    print("Run continued: Y")


# ---------------------------------------------------------
# FAULT 1: INVALID JSON
# ---------------------------------------------------------

fault_1 = make_tool_call(
    "get_weather",
    '{"city": "Chennai", "unit": "C"'
)


# ---------------------------------------------------------
# FAULT 2: UNKNOWN TOOL
# ---------------------------------------------------------

fault_2 = make_tool_call(
    "get_temperature",
    json.dumps({
        "city": "Chennai",
        "unit": "C"
    })
)


# ---------------------------------------------------------
# FAULT 3: MISSING REQUIRED ARGUMENT
# ---------------------------------------------------------

fault_3 = make_tool_call(
    "get_weather",
    json.dumps({
        "city": "Chennai"
    })
)


# ---------------------------------------------------------
# FAULT 4: WRONG TYPE
# ---------------------------------------------------------

fault_4 = make_tool_call(
    "get_weather",
    json.dumps({
        "city": 123,
        "unit": "C"
    })
)


# ---------------------------------------------------------
# FAULT 5: INVALID ENUM VALUE
# ---------------------------------------------------------

fault_5 = make_tool_call(
    "get_weather",
    json.dumps({
        "city": "Chennai",
        "unit": "K"
    })
)


# ---------------------------------------------------------
# FAULT 6: INVENTED ARGUMENT
# ---------------------------------------------------------

fault_6 = make_tool_call(
    "get_weather",
    json.dumps({
        "city": "Chennai",
        "unit": "C",
        "temperature": 30
    })
)


# ---------------------------------------------------------
# FAULT 7: NEGATIVE DAYS
#
# This demonstrates an important point:
# the current schema checks that days is an integer,
# but it does not check business meaning.
# ---------------------------------------------------------

fault_7 = make_tool_call(
    "calculate_budget",
    json.dumps({
        "transport": 1500,
        "accommodation_per_day": 1200,
        "food_per_day": 500,
        "days": -2,
        "currency": "Rs"
    })
)


# ---------------------------------------------------------
# FAULT 8: WRONG TYPE FOR DAYS
# ---------------------------------------------------------

fault_8 = make_tool_call(
    "calculate_budget",
    json.dumps({
        "transport": 1500,
        "accommodation_per_day": 1200,
        "food_per_day": 500,
        "days": "two",
        "currency": "Rs"
    })
)


# ---------------------------------------------------------
# RUN ALL FAULTS
# ---------------------------------------------------------

if __name__ == "__main__":

    faults = [
        ("Invalid JSON", fault_1),
        ("Unknown tool", fault_2),
        ("Missing required argument", fault_3),
        ("Wrong type", fault_4),
        ("Value outside enum", fault_5),
        ("Invented argument", fault_6),
        ("Invalid business value", fault_7),
        ("Wrong type for days", fault_8)
    ]

    print("\nFAULT INJECTION TEST")
    print("No model or internet is required.")

    for number, (name, tool_call) in enumerate(
        faults,
        start=1
    ):

        run_fault_test(
            number,
            name,
            tool_call
        )
        
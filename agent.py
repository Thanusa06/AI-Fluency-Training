import json

from config import client, MODEL, QUESTIONS, banner
from tools import TOOLS, TOOL_FUNCTIONS


SYSTEM_PROMPT = (
    "You are a college fee assistant.\n"
    "Never guess a fee. Always use get_course_fee to get a course fee.\n"
    "Use calculator for all arithmetic calculations.\n"
    "Available course codes: CS101, AI202, DS303.\n"
    "Call only the exact tool names provided in the tools list.\n"
    "The exact tool names are: get_course_fee and calculator.\n"
    "Do not add anything to the tool name.\n"
    "If no tool is needed, answer directly."
)


def agent(question, max_steps=6, verbose=True):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for step in range(1, max_steps + 1):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0,
            parallel_tool_calls=False,
            reasoning_effort="low"
        )

        message = response.choices[0].message

        # No tool call -> final answer
        if not message.tool_calls:
            return message.content.strip()

        # Add assistant message containing tool call
        messages.append({
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": [
                {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": call.function.name,
                        "arguments": call.function.arguments
                    }
                }
                for call in message.tool_calls
            ]
        })

        # Execute the tool
        for call in message.tool_calls:

            name = call.function.name

            # Safety check for malformed tool names
            if "<|channel|>" in name:
                name = name.split("<|channel|>")[0]

            arguments = json.loads(
                call.function.arguments or "{}"
            )

            function = TOOL_FUNCTIONS.get(name)

            if function is None:
                result = f"Unknown tool: {name}"
            else:
                result = function(**arguments)

            if verbose:
                print(
                    f"   step {step}: "
                    f"{name}({arguments}) -> {result}"
                )

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": result
            })

    return "Stopped: maximum steps reached without a final answer."


if __name__ == "__main__":

    banner("SYSTEM 3: AI AGENT")

    for question in QUESTIONS:

        print("Q:", question)

        print("A:", agent(question))

        print("-" * 70)
"""Day 3: a ReAct agent written from scratch.
No guards yet - it will fail on purpose.
"""

import json

from config import client, MODEL, banner
from my_tools import TOOLS, TOOL_FUNCTIONS


SYSTEM_PROMPT = """
You are a ReAct-style agent.

You can use these tools:
- calculator
- read_webpage

Think about what tool is needed, call the tool, observe the result,
and then give the final answer.

If a requested tool does not exist, this experiment will demonstrate
what happens when the agent tries to access an unknown tool.


"""


def agent(question, max_steps=6):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    for step in range(1, max_steps + 1):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )

        message = response.choices[0].message

        # If the model wants to call a tool
        if message.tool_calls:
            messages.append(message)

            for call in message.tool_calls:
                name = call.function.name

                try:
                    arguments = call.function.arguments

                    import json
                    args = json.loads(arguments)

                    print(
                        f"   step {step}: {name}({args})",
                        end=" -> "
                    )

                    # INTENTIONALLY UNSAFE FOR FAILURE 2
                    function = TOOL_FUNCTIONS.get(name)

                    result = function(**args)

                    print(result)

                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": call.id,
                            "content": str(result),
                        }
                    )

                except Exception as e:
                    print(f"ERROR: {e}")
                    return f"Agent stopped because of error: {e}"

        else:
            answer = message.content
            return answer

    return "Agent stopped: maximum steps reached."


if __name__ == "__main__":
    banner("MY AGENT (no guards)")

    question = (
        "Read notice.html and tell me the total fee for CS101 "
        "and AI202 after the merit scholarship."
    )

    print("Q:", question)
    print("A:", agent(question))
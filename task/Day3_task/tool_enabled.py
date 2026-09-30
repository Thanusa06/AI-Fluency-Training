import json

from config import client, MODEL
from tools import get_subject_mark


TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_subject_mark",
        "description": (
            "Look up Arun's mark for a subject from the local "
            "student data file. Use this when the user asks "
            "for a specific subject mark."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "subject": {
                    "type": "string",
                    "description": "Subject name, such as Maths, Python, C, or AI."
                }
            },
            "required": ["subject"]
        }
    }
}


QUESTIONS = [
    "What are some effective ways to improve in mathematics?",
    "What is Arun's Maths mark?",
    "Why is it useful to track your subject marks?"
]


for question in QUESTIONS:
    print("\n" + "=" * 60)
    print("QUESTION:", question)
    print("=" * 60)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful student assistant. "
                "You have access to one tool called get_subject_mark. "
                "Use the tool when the user asks for a specific "
                "student subject mark. Do not invent private marks."
            )
        },
        {
            "role": "user",
            "content": question
        }
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=[TOOL_SCHEMA],
        tool_choice="auto"
    )

    assistant_message = response.choices[0].message
    messages.append(assistant_message)

    if assistant_message.tool_calls:
        for tool_call in assistant_message.tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            print("TOOL CALL:", tool_name)
            print("TOOL ARGUMENTS:", arguments)

            if tool_name == "get_subject_mark":
                tool_result = get_subject_mark(**arguments)
            else:
                tool_result = "Error: Unknown tool."

            print("TOOL RESULT:", tool_result)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result
                }
            )

        final_response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )

        final_answer = final_response.choices[0].message.content

    else:
        print("TOOL CALL: None")
        final_answer = assistant_message.content

    print("FINAL ANSWER:", final_answer)

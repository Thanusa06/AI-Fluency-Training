
import json
import operator
from typing import Annotated, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from lc_config import (
    MODEL,
    PROVIDER,
    GROQ_API_KEY,
    EMBEDDING_MODEL,
    CHROMA_DB_DIR,
    MAX_DISTANCE,
)

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings


# --------------------------------------------------
# 1. Connect to the existing handbook vector database
# --------------------------------------------------

embeddings = FastEmbedEmbeddings(model_name=EMBEDDING_MODEL)

store = Chroma(
    collection_name="day8_task_handbook",
    persist_directory=str(CHROMA_DB_DIR),
    embedding_function=embeddings,
)


# --------------------------------------------------
# 2. Handbook search tool
# --------------------------------------------------

@tool
def search_handbook(query: str) -> str:
    """Search the college handbook for policy information."""

    results = store.similarity_search_with_score(query, k=3)

    matching_results = []

    for document, score in results:
        if score <= MAX_DISTANCE:
            source = document.metadata.get("source", "unknown")
            matching_results.append(
                f"Source: {source}\n"
                f"Distance score: {score:.4f}\n"
                f"Content: {document.page_content}"
            )

    if not matching_results:
        return "NO_MATCH: this is not covered in the college handbook"

    return "\n\n".join(matching_results)


# --------------------------------------------------
# 3. Attendance eligibility tool
# --------------------------------------------------

@tool
def check_exam_eligibility(attendance_percent: float) -> str:
    """Check exam eligibility using attendance percentage.
    Invalid percentages are outside 0 to 100.
    At least 75% is eligible.
    From 65% to below 75% requires Rs. 500 condonation
    per course.
    Below 65% is not eligible.
    """

    if attendance_percent < 0 or attendance_percent > 100:
        return "ERROR: attendance must be between 0 and 100."

    if attendance_percent >= 75:
        return (
            f"Attendance is {attendance_percent}%. "
            "Eligible to write the examination."
        )

    if attendance_percent >= 65:
        return (
            f"Attendance is {attendance_percent}%. "
            "Eligible after applying for condonation. "
            "Fee: Rs. 500 per course."
        )

    return (
        f"Attendance is {attendance_percent}%. "
        "Not eligible to write the examination."
    )


# --------------------------------------------------
# 4. Calculator tool
# --------------------------------------------------

@tool
def calculator(expression: str) -> str:
    """Calculate a basic arithmetic expression using safe operations.
    Supports numbers and +, -, *, / operations.
    """

    try:
        import ast

        def calculate(node):
            if isinstance(node, ast.Expression):
                return calculate(node.body)

            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)):
                    return node.value
                raise ValueError("Only numbers are allowed.")

            if isinstance(node, ast.BinOp):
                left = calculate(node.left)
                right = calculate(node.right)

                operations = {
                    ast.Add: operator.add,
                    ast.Sub: operator.sub,
                    ast.Mult: operator.mul,
                    ast.Div: operator.truediv,
                }

                operation = operations.get(type(node.op))
                if operation is None:
                    raise ValueError("Unsupported operation.")

                return operation(left, right)

            if isinstance(node, ast.UnaryOp):
                value = calculate(node.operand)

                if isinstance(node.op, ast.UAdd):
                    return value
                if isinstance(node.op, ast.USub):
                    return -value

            raise ValueError("Invalid arithmetic expression.")

        tree = ast.parse(expression, mode="eval")
        answer = calculate(tree)

        return str(answer)

    except Exception as error:
        return f"Calculation error: {error}"


# --------------------------------------------------
# 5. Course fee lookup tool
# --------------------------------------------------

@tool
def get_course_fee(course_code: str) -> str:
    """Get the fee for a known course code from the sample handbook."""

    fees = {
        "CS101": 12000,
        "AI202": 18000,
        "DS303": 15000,
    }

    course_code = course_code.strip().upper()

    if course_code not in fees:
        return f"ERROR: no fee found for course {course_code}."

    return f"{course_code} fee: Rs. {fees[course_code]}"


# --------------------------------------------------
# 6. Register tools and configure the language model
# --------------------------------------------------

tools = [
    search_handbook,
    check_exam_eligibility,
    calculator,
    get_course_fee,
]

if PROVIDER.lower() == "groq":
    from langchain_groq import ChatGroq

    llm = ChatGroq(
        model=MODEL,
        api_key=GROQ_API_KEY,
        temperature=0,
    )
else:
    raise ValueError(
        f"Unsupported provider in this task: {PROVIDER}. "
        "This code currently configures Groq."
    )

llm_with_tools = llm.bind_tools(tools)


# --------------------------------------------------
# 7. Define the agent state and graph
# --------------------------------------------------

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]


SYSTEM_PROMPT = """
You are a college handbook assistant.

Rules:
1. Use search_handbook for handbook and placement policy questions.
2. Use check_exam_eligibility for attendance eligibility questions.
3. Use get_course_fee to look up course fees.
4. Use calculator for arithmetic calculations.
5. If a tool returns NO_MATCH, say that you do not know
   because the information is not covered in the handbook.
6. Never invent college policies or fees.
7. Remember relevant earlier messages in the same conversation.
8. Give clear, concise answers based on tool results.
"""


def assistant_node(state: AgentState):
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        *state["messages"],
    ]

    response = llm_with_tools.invoke(messages)

    return {"messages": [response]}


def should_continue(state: AgentState):
    last_message = state["messages"][-1]

    if getattr(last_message, "tool_calls", None):
        return "tools"

    return END


builder = StateGraph(AgentState)

builder.add_node("assistant", assistant_node)
builder.add_node("tools", ToolNode(tools))

builder.set_entry_point("assistant")

builder.add_conditional_edges(
    "assistant",
    should_continue,
    {"tools": "tools", END: END},
)

builder.add_edge("tools", "assistant")

agent = builder.compile()


# --------------------------------------------------
# 8. Test the attendance tool directly
# --------------------------------------------------

if __name__ == "__main__":
    print("DAY 8 TASK AGENT")
    print("=" * 60)

    print("\nATTENDANCE TOOL TESTS")

    for attendance in [82, 70, 50, 120]:
        print(
            f"{attendance}% -> "
            f"{check_exam_eligibility.invoke({'attendance_percent': attendance})}"
        )

    # Use the same thread ID for all questions so conversation
    # context can be preserved in this run.
    questions = [
        "What CGPA do I need to be eligible for placements?",
        "My attendance is 70%. Can I write the exam?",
        (
            "What is the total of the CS101 fee, the AI202 fee "
            "and the maximum late fee?"
        ),
        "And if I pay only 5 days late instead?",
        "What is the capital of France?",
    ]

    print("\nAGENT QUESTION TESTS")
    print("=" * 60)

    conversation = []

    for number, question in enumerate(questions, start=1):
        print(f"\nQUESTION {number}: {question}")

        conversation.append(HumanMessage(content=question))

        try:
            result = agent.invoke({"messages": conversation})

            conversation = result["messages"]

            for message in conversation:
                if getattr(message, "tool_calls", None):
                    for tool_call in message.tool_calls:
                        print(f"Tool called: {tool_call['name']}")

            final_message = conversation[-1]
            print(f"ANSWER: {final_message.content}")

        except Exception as error:
            print(f"ERROR: {error}")
            break


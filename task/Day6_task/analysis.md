# Day 6 Task
# Reliable Tool Calling: Schemas, Validation, Retry and Structured Outputs

## Scenario: Weekend Trip Assistant

### 1. Introduction

For this task, I built a small Weekend Trip Assistant.

The assistant helps a user plan a short trip. It has two tools:

1. `get_weather`
2. `calculate_budget`

The weather tool returns simple weather information for a destination city.

The budget tool calculates the total trip cost using transport, accommodation, food, number of days and currency.

The main purpose of this project is not the size of the application. The purpose is to demonstrate that a model-generated tool call cannot be trusted directly. The model only generates a request describing which function it wants to use and what arguments it wants to send. My Python program is responsible for checking those arguments and actually executing the function.

The project therefore adds validation, error messages, retry behaviour, repeated-call protection and structured output experiments.

---

# 2. Explanation of Concepts

## 2.1 What is the Chat Completions format?

Chat Completions is a request/response format where my Python program sends a list of messages to a model.

The main request fields used in my project are:

- `model`
- `messages`
- `tools`
- `tool_choice`
- `parallel_tool_calls`
- `max_tokens`
- `temperature`

The `messages` list contains different message roles such as:

- `system`
- `user`
- `assistant`
- `tool`

For example, the user can ask:

> What is the weather in Chennai?

The model may decide that it needs the `get_weather` tool.

The response contains choices. A choice contains an assistant message and a `finish_reason`.

The important finish reasons for this task are:

### `stop`

This means the model finished its response normally.

If there are no tool calls, my program can use the assistant's content as the final answer.

### `length`

This means the response was stopped because the token limit was reached.

My program does not treat this as a normal final answer. Instead, it increases `max_tokens` and retries.

### `tool_calls`

This means the model wants my program to execute one or more tools.

The important point is that the model does not execute the Python function itself.

When the model wants a tool, `message.content` can be empty because the assistant is communicating through structured tool-call information instead of normal text.

In my program, I check `message.tool_calls` rather than assuming that `message.content` will contain the answer.

---

# 2.2 What does OpenAI-compatible mean?

An OpenAI-compatible server provides an API with a similar request and response format to the OpenAI API.

This means the same Python `openai` client can often communicate with different providers by changing the server URL and model configuration.

For example, my program uses:

```python
client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)

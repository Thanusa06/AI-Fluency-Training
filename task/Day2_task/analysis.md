# Day 2 Task – Comparing Direct Prompting, Chain-of-Thought, and ReAct

## 1. Scenario

The scenario selected for this experiment is a weekend trip planner for Chennai.

The user has a total budget of ₹5000. The task involves calculating travel and accommodation expenses and, for the ReAct approach, obtaining current Chennai weather using an external weather tool.

The goal is to compare Direct Prompting, Chain-of-Thought, and a ReAct agent in terms of reasoning, tool usage, reliability, transparency, speed, cost, and consistency.

---

## 2. Direct Prompting

Direct Prompting gives the model the complete question and asks it to provide the answer directly without using external tools.

For this experiment, the model was asked:

- Total budget = ₹5000
- Travel cost = ₹1500
- Accommodation cost = ₹1200
- Number of places visited on Saturday = 3
- Number of places visited on Sunday = 2

The model returned:

- Remaining money = ₹2300
- Total places visited = 5

The calculation is:

₹5000 - ₹1500 - ₹1200 = ₹2300

And:

3 + 2 = 5

Direct Prompting was sufficient for these simple calculations because no external information was required.

---

## 3. Chain-of-Thought

The Chain-of-Thought approach was used for a multi-step calculation involving several expenses.

The scenario included:

- Total budget = ₹5000
- Travel = ₹1500
- Accommodation = ₹1200
- Food = ₹800
- Souvenirs = ₹500

The remaining amount is:

₹5000 - ₹1500 - ₹1200 - ₹800 - ₹500 = ₹1000

This approach is useful when a task contains multiple dependent calculation steps. Instead of only asking for a final answer, the prompt encourages the model to handle the problem systematically.

For this experiment, the reasoning can be evaluated from the final calculation and result rather than requiring the model to expose private chain-of-thought.

---

## 4. ReAct Agent

The ReAct approach combines reasoning with actions and observations.

In this experiment, the agent first identified that it needed to calculate the remaining budget and obtain current weather information.

The execution followed this pattern:

1. Thought – The agent identified the required tasks.
2. Action – The agent called the Chennai weather tool.
3. Observation – The tool returned the current weather information.
4. Final Answer – The agent combined the calculation and tool result.

The observed output was:

- Remaining budget = ₹2300
- Chennai temperature = 30.1°C
- Weather condition = Overcast

The weather information was obtained using the external weather tool rather than being generated only from the language model.

---

## 5. Comparison

| Criteria | Direct Prompting | Chain-of-Thought | ReAct Agent |
|---|---|---|---|
| Reasoning depth | Low | Medium | Medium to High |
| Tool usage | No | No | Yes |
| Reliability | Good for simple tasks | Good for multi-step calculations | Useful when external information is required |
| Transparency | Shows final answer | Shows calculation/explanation | Shows actions and observations |
| Speed/Cost | Fast and low cost | More reasoning may require more tokens | May take longer because of tool calls |
| Consistency | High for simple questions | Generally good for structured calculations | Depends on both reasoning and tool results |

---

## 6. Self-Consistency Experiment

A self-consistency experiment was performed by asking the same calculation question multiple times.

### Temperature 0.7

Five runs were performed:

- Run 1: ₹1000
- Run 2: ₹1000
- Run 3: ₹1000
- Run 4: ₹1000
- Run 5: ₹1000

Result: 5 out of 5 runs produced ₹1000.

### Temperature 0

Three runs were performed:

- Run 1: ₹1000
- Run 2: ₹1000
- Run 3: ₹1000

Result: 3 out of 3 runs produced ₹1000.

### Observation

Both temperature settings produced the same answer for this particular arithmetic problem. This shows that the question was simple enough for the model to remain consistent even when sampling at a nonzero temperature.

The experiment does not prove that all questions will produce the same level of consistency. More complex or ambiguous questions may produce different results.

---

## 7. When Each Approach Is Suitable

### Direct Prompting

Direct Prompting is suitable when the task is simple, clearly defined, and does not require external information.

Examples include:

- Simple calculations
- Basic text generation
- Short question answering
- Straightforward transformations

### Chain-of-Thought

A structured reasoning approach is useful when a problem contains multiple steps or requires careful calculation.

Examples include:

- Multi-step arithmetic
- Planning problems
- Logical reasoning
- Problems involving several constraints

### ReAct

ReAct is useful when the task requires interaction with external tools or up-to-date information.

Examples include:

- Weather information
- Searching external information
- Calling APIs
- Using calculators or databases
- Tasks that require multiple actions

---

## 8. Conclusion

The experiment demonstrated that different prompting and agent approaches are useful for different types of tasks.

Direct Prompting handled simple calculations quickly and successfully.

The structured reasoning approach was useful for the multi-step budget calculation.

The ReAct approach demonstrated an additional capability: using an external weather tool and incorporating the observation into the final response.

The self-consistency experiment produced the same answer across all tested runs at both temperature 0.7 and temperature 0. Therefore, for this particular simple arithmetic task, the model showed consistent results.

Overall, the experiment demonstrates the difference between answering a question directly, performing multi-step reasoning, and interacting with external tools through an agent-style workflow.
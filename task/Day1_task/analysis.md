# Comparing a Plain Chatbot, a Rule-Based Workflow, and an AI Agent

## 1. Introduction

For this project, I selected a private student-data scenario. The private data is stored in a JSON file named `student_data.json`. The file contains information such as the student's name, student ID, department, year, attendance, CGPA, pending assignments, and pending fees.

The same student-data problem is demonstrated using three approaches: a plain chatbot, a rule-based workflow, and an AI agent. This comparison shows how these approaches differ in flexibility, decision-making, tool usage, private-data access, multi-step task handling, automation, and reliability.

---

## 2. Private-Data Scenario

The chosen scenario is a student information assistant.

The private student information is stored in `Data/student_data.json`. The data includes the student's name, department, year, attendance percentage, CGPA, pending assignments, and pending fees.

For example, a student may ask:

> "What is my attendance?"

> "Do I have pending assignments?"

> "What is my student status?"

This scenario is useful because the system needs to work with private student information.

---

## 3. Plain Chatbot

A plain chatbot mainly uses an LLM to understand a user's question and generate a response.

In this project, the user asks the chatbot about their attendance. The chatbot does not directly access the private `student_data.json` file. Therefore, it cannot automatically retrieve the student's actual attendance.

The plain chatbot does not use a private-data tool in this implementation. It mainly receives the user's question and generates a conversational response.

The process is:

**User Question → Chatbot → Response**

The main limitation is that the chatbot cannot access private student information unless an appropriate data connection or tool is provided. It is useful for general questions and explanations, but it is limited when the answer requires information stored in a private file.

---

## 4. Rule-Based Workflow

A rule-based workflow follows predefined steps and conditions. It does not use an LLM.

In this project, the workflow reads the student's information from `student_data.json`. It retrieves the attendance percentage and applies predefined conditions.

For example, if attendance is below 75%, the workflow reports that attendance is below the required level. If attendance is between 75% and 85%, it reports that attendance needs improvement. If attendance is above 85%, it reports that attendance is good.

The process is:

**Read Data → Apply Rules → Generate Result**

The main advantage of this approach is predictable behaviour. The same input and the same rules produce the same result.

However, the workflow has limited flexibility. If a new type of question is asked, new rules and code may need to be added.

---

## 5. AI Agent

An AI agent combines an LLM with tools and a loop.

In this project, the agent can use a tool to read the private student data. It can then use another tool to check the student's status.

The agent starts with the user's request. It selects an appropriate tool, receives the result, observes the information, and can continue with another action before producing the final response.

The process can be represented as:

**User Request → Agent → Tool → Observation → Next Action → Final Response**

The main concept is:

**Agent = LLM + Tools + Loop**

The agent can therefore handle tasks that require multiple steps and tool usage.

The main limitation is that the tools must be correctly designed and the agent needs appropriate permissions to access private information.

---

## 6. Comparison Table

| Basis for comparison     | Plain chatbot                                                                                  | Rule-based workflow                   | AI agent                                                       |
| ------------------------ | ---------------------------------------------------------------------------------------------- | ------------------------------------- | -------------------------------------------------------------- |
| Flexibility              | Can understand many natural-language questions, but has no private-data access in this project | Limited to predefined rules           | More flexible because it can choose actions and tools          |
| Decision-making          | Generates a response using the language model                                                  | Uses predefined conditions            | Uses reasoning, tools, and observations                        |
| Tool usage               | No private-data tool                                                                           | Uses code to read the JSON file       | Uses tools to access and process data                          |
| Private-data access      | Cannot directly access the private JSON file                                                   | Can directly read the JSON file       | Can access private data through tools                          |
| Multi-step task handling | Mainly handles the current conversation                                                        | Follows fixed steps                   | Can perform multiple actions using a loop                      |
| Automation               | Low for private-data tasks                                                                     | Automates predefined tasks            | Can automate more dynamic multi-step tasks                     |
| Reliability              | Depends on the information available to the chatbot                                            | Predictable for clearly defined rules | Depends on the correctness of tools, reasoning, and safeguards |

---

## 7. Suitability Analysis

Each approach is useful for a different type of problem.

A plain chatbot is useful when the student needs general explanations or conversational assistance. For example, it can explain what attendance percentage or CGPA means. However, in this project it cannot directly access the student's private information.

A rule-based workflow is useful when the task has clear and fixed conditions. For example, checking whether attendance is below 75% can be handled using predefined rules.

An AI agent is useful when the task requires private-data access and multiple steps. For example, an agent could read the student's attendance, check pending assignments, check fees, and then provide a combined student status.

Therefore, the appropriate approach depends on the problem. A simple question may only require a chatbot. A predictable process can use a rule-based workflow. A dynamic task involving multiple tools and actions can use an AI agent.

---

## 8. Limitations

The plain chatbot cannot directly retrieve private student information in this implementation because it has no private-data tool.

The rule-based workflow can access private data, but its behaviour depends on predefined rules. If the requirements change, the programmer may need to modify the rules.

The AI agent can handle more flexible and multi-step tasks, but its reliability depends on the quality of its tools, instructions, data, and safeguards. Private student information must also be protected and only accessed when necessary.

---

## 9. Conclusion

A plain chatbot, a rule-based workflow, and an AI agent solve problems in different ways.

A plain chatbot is suitable for conversational tasks, general questions, and explanations.

A rule-based workflow is suitable for predictable and repetitive tasks where the steps and conditions can be defined in advance.

An AI agent is suitable for dynamic and multi-step tasks where the system needs to use tools, observe results, decide what to do next, and continue until the task is completed.

The main concept demonstrated in this project is:

**Plain Chatbot → LLM response**

**Rule-Based Workflow → Predefined rules and conditions**

**AI Agent → LLM + Tools + Loop**

Therefore, the choice of approach should depend on the requirements of the problem rather than using an AI agent for every task.


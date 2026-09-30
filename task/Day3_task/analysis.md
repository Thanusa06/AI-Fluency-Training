\# Day 3 Task — From Prompt to Action: Understanding LLMs, Tools, and Agents



\## 1. Scenario



I created a small \*\*Student Marks Assistant\*\*.



The student data is stored in a local JSON file:



`data/student\_data.json`



The data contains marks for Arun:



\- C: 45

\- Python: 72

\- Maths: 38

\- AI: 81



The experiment compares:



1\. A plain LLM without any external tool.

2\. The same LLM with one external tool called `get\_subject\_mark`.



The purpose is to observe when the LLM can answer by itself and when it needs external data.



\---



\## 2. LLM



An \*\*LLM (Large Language Model)\*\* is a model that generates text responses based on patterns learned during training and the information provided in the current conversation.



A plain LLM does not automatically have access to my local files.



For example, when I asked:



> What is Arun's Maths mark?



the plain LLM could not access `student\_data.json`, so it said that it did not have the information.



Therefore, an LLM should not invent private or local data that it cannot access.



\---



\## 3. Agent



An \*\*AI agent\*\* is a system where an LLM can use available tools to perform actions or obtain information when needed.



In this experiment, the LLM can decide whether it needs the `get\_subject\_mark` tool.



For a general question such as:



> What are some effective ways to improve in mathematics?



the model did not need the tool.



For the question:



> What is Arun's Maths mark?



the model used the tool because the answer depended on local student data.



\---



\## 4. Tool



A \*\*tool\*\* is an external function that an LLM can call to obtain information or perform an action.



This project uses exactly one tool:



`get\_subject\_mark(subject)`



The tool reads `data/student\_data.json` and returns the requested student's subject mark as plain text.



Example:



```text

get\_subject\_mark("Maths")




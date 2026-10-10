# Day 8 Task Results

## Configuration

- Provider: `groq`
- Model: `openai/gpt-oss-120b`
- Embedding model: `BAAI/bge-small-en-v1.5`
- MAX_DISTANCE: `0.8`
- Placement question distance score: `0.2962`
- France question distance score: `1.2226`

## Part A: Placement Policy Search

Question: What CGPA do I need to be eligible for placements?

- Expected answer: 6.5 CGPA or above, with no standing arrears.
- Top result source: `placement_policy.md`
- Correct: Yes

## Part B: Exam Eligibility Tool

| Attendance | Actual result |
|---:|---|
| 82% | ELIGIBLE |
| 70% | CONDONATION; Rs. 500 per course |
| 50% | NOT ELIGIBLE |
| 120% | Error: attendance must be between 0 and 100 |

## Part C: Distance Threshold

- Placement question score: `0.2962`
- France question score: `1.2226`
- Selected MAX_DISTANCE: `0.8`
- Reason: The placement question's distance is below 0.8, so it passes the threshold. The France question's distance is above 0.8, so it should be rejected as unrelated to the handbook.

## Part D: Agent Test Results

| # | Question | Agent's answer (short) | Correct? |
|---|---|---|---|
| 1 | Placement CGPA | CGPA 6.5 or higher, with no standing arrears | Yes |
| 2 | 70% attendance | Eligible after condonation; Rs. 500 per course | Yes |
| 3 | CS101 + AI202 + maximum late fee | Rs. 32,000 | Yes |
| 4 | Five-day late payment | Rs. 30,500 total | Yes |
| 5 | Capital of France | Refused because it is not covered in the college handbook | Yes |

## Issues and Observations

- The agent answered the five test questions appropriately.
- Attendance validation handled normal, low, and invalid attendance values.
- The France question was rejected because it was outside the handbook's coverage.
- LangChain displayed deprecation warnings for the Chroma integration. They did not stop execution.
- The displayed tool-call list repeats earlier calls, so it should be corrected before recording exact tool sequences.


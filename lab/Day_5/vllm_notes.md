# Day 5 - Model Serving and vLLM Notes

## Environment

This Day 5 implementation uses the Groq API instead of Ollama.

Ollama was not installed or used.

The Ollama Modelfile section is included as a conceptual comparison.

The vLLM section is completed as a theory/instructor-demonstration
section because full vLLM serving normally requires a suitable GPU
environment.

---

# Part A - Model Serving

## Original task

The original Day 5 lab asks students to use Ollama to:

- Pull models
- Run models
- Inspect models
- Stop models
- Remove models
- Compare model sizes
- Inspect context length
- Inspect licenses

## Alternative implementation

This project uses Groq as the model-serving provider.

The Python application connects to the Groq OpenAI-compatible API.

Provider:

```text
Groq

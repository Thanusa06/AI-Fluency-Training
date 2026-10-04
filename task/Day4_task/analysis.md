# Day 4 Task — Will It Fit, and May I Use It?

## Scenario

I want to run a local AI college-fee assistant on my laptop.

- Machine: Laptop with 8 GB available memory
- Purpose: Answer college-course fee questions
- User: Myself
- Memory budget: 8 GB
- Requirement: The model should fit within the available memory and have a suitable licence.

## 3.1 Explanation of Each Concept

### 1. Model Weights

Model weights are the numerical values learned by an AI model. The number of
parameters and the precision used to store them determine how much memory the
model weights require.

In my scenario, I used the Day 4 memory formula:

Weights = Parameters × Bytes per parameter

For example, an 8B model using Q4_K_M has:

8 × 0.57 = 4.56 GB

Therefore, the model weights require approximately 4.56 GB.

If I ignore model weights, I may choose a model that is too large for my
8 GB laptop.

The limitation is that the weight calculation only estimates the memory
required for the model weights. It does not include the KV cache or runtime
overhead.

### 2. Quantization

Quantization means storing model parameters using fewer bits or fewer bytes.
This reduces the amount of memory needed by the model.

In my scenario, I compared different precisions for the same 8B model at 8K
context. For example:

- Q3_K_M = 0.43 bytes per parameter
- Q4_K_M = 0.57 bytes per parameter
- Q5_K_M = 0.68 bytes per parameter
- Q8_0 = 1.00 byte per parameter
- FP16 = 2.00 bytes per parameter

For the 8B model, Q4_K_M required 4.56 GB for weights, while FP16 required
16.00 GB. Therefore, Q4_K_M saves a large amount of memory.

If I ignore quantization, I may choose FP16 and the model may not fit on my
8 GB laptop.

The limitation is that using lower precision can involve a trade-off in model
quality. Therefore, I should choose a quantization that reduces memory while
still providing acceptable quality for my task.

### 3. KV Cache and Context Length

The KV cache is memory used to keep information from previous tokens while the
model is generating an answer. Context length is the amount of text or tokens
the model can consider at one time.

In my scenario, I used the Day 4 formula:

KV cache = Parameters × Context (K) × 0.02

For an 8B Q4_K_M model:

At 8K context:

8 × 8 × 0.02 = 1.28 GB

At 32K context:

8 × 32 × 0.02 = 5.12 GB

At 128K context:

8 × 128 × 0.02 = 20.48 GB

The weights remain 4.56 GB, but the KV cache increases as the context length
increases. Therefore, a model that fits at a short context can stop fitting at
a long context.

If I ignore context length, I may think an 8B Q4_K_M model will always fit
within my 8 GB memory budget. This would be incorrect for a very long context.

The limitation is that the KV-cache formula is an approximation. Actual memory
usage can differ depending on the model architecture and runtime.

### 4. Model Card

A model card is a document that provides important information about an AI
model. It can contain information such as the model name, publisher,
parameters, context length, licence, supported capabilities and usage
information.

In my scenario, I used model cards to compare open models before choosing a
model. I checked information such as the licence, context window and tool
calling support.

If I ignore the model card, I may choose a model only because it is small
enough to fit in memory, without checking whether its licence and capabilities
are suitable for my project.

The limitation is that model cards contain information provided by the model
publisher, and the information or licence can be updated. Therefore, I record
the date on which I checked the model card.

### 5. Open-weight vs Open-source Licensing

Open-weight means that the model weights are available for people to download
and run. This does not automatically mean that the model has an open-source
licence.

Open-source licensing means that the exact licence and its conditions determine
what users are allowed to do with the model, such as commercial use,
modification and redistribution.

In my scenario, I checked the exact licence of the models before choosing one.
For example, I compared models that use the Apache License 2.0.

If I ignore the licence, I could choose a model that fits my 8 GB laptop but
still cannot legally use it for my intended project.

The limitation is that "open-weight" alone does not tell me what permissions I
have. I must read the exact licence and its conditions before using or
redistributing a model.

## 3.2 Memory Estimate

I used the Day 4 memory-estimation formula:

Weights = Parameters × Bytes per parameter

KV cache = Parameters × Context (K) × 0.02

Total memory = (Weights + KV cache) × 1.10

I used an available memory budget of 8 GB.

| Model configuration | Parameters | Precision | Context | Weights (GB) | KV Cache (GB) | Total (GB) | Fit on 8 GB? |
|---|---:|---|---:|---:|---:|---:|---|
| Small model | 1.5B | Q4_K_M | 8K | 0.85 | 0.24 | 1.20 | Yes |
| Mid model | 8B | Q4_K_M | 8K | 4.56 | 1.28 | 6.42 | Yes, but tight |
| Mid model FP16 | 8B | FP16 | 8K | 16.00 | 1.28 | 19.01 | No |
| Large model | 30B | Q4_K_M | 8K | 17.10 | 4.80 | 24.09 | No |
| Very large model | 70B | Q4_K_M | 8K | 39.90 | 11.20 | 56.21 | No |

### Interpretation

The 1.5B Q4_K_M configuration fits comfortably within my 8 GB memory budget.

The 8B Q4_K_M configuration requires approximately 6.42 GB, so it fits within
8 GB but leaves limited memory for other applications.

The same 8B model using FP16 requires approximately 19.01 GB, so it does not
fit within my 8 GB memory budget.

The 30B and 70B Q4_K_M configurations are also too large for my laptop.

Therefore, for my college-fee assistant scenario, a smaller quantized model is
more practical than a large or full-precision model.

### Model Comparison

I compared four models from different model families:

1. Qwen3-8B
2. Mistral 7B Instruct v0.3
3. IBM Granite-3.3-8B-Instruct
4. gpt-oss-20b

| Model | Publisher | Parameters | Context | Licence | Commercial Use | Tool Calling | Ollama |
|---|---|---:|---:|---|---|---|---|
| Qwen3-8B | Qwen / Alibaba | ~8B | 40K | Apache-2.0 | Yes | Yes | Yes |
| Mistral 7B Instruct v0.3 | Mistral AI | 7B | 32K | Apache-2.0 | Yes | Yes | Yes |
| IBM Granite-3.3-8B-Instruct | IBM | 8B | 128K | Apache-2.0 | Yes | Yes | Yes |
| gpt-oss-20b | OpenAI | 20.9B total / 3.6B active | 128K | Apache-2.0 | Yes | Yes | Yes |

For the memory comparison, I used the Day 4 estimation formula with an 8K
context. The estimated memory values help me decide whether each model is
suitable for my 8 GB laptop.

| Model | Q4 Download Size | Estimated Memory at 8K | Fits 8 GB? |
|---|---:|---:|---|
| Qwen3-8B | ~5.2 GB | ~6.42 GB | Yes, but tight |
| Mistral 7B Instruct v0.3 | ~4.4 GB | ~5.72 GB | Yes |
| IBM Granite-3.3-8B-Instruct | ~4.94 GB | ~6.42 GB* | Yes* |
| gpt-oss-20b | ~14 GB | Does not fit | No |

*Granite's 128K context would require much more KV-cache memory than the 8K
estimate shown here. Therefore, I would use a much smaller context on an 8 GB
laptop.

### Model Comparison Analysis

Qwen3-8B and Mistral 7B Instruct v0.3 are practical candidates for my
college-fee assistant because they are available in quantized formats and use
the Apache-2.0 licence.

Mistral 7B Instruct v0.3 has the lowest estimated memory requirement among the
models compared here, making it attractive for an 8 GB laptop.

Qwen3-8B is also a possible choice, but its estimated memory usage is close to
the 8 GB limit.

IBM Granite provides a very large context window, but a long context can
increase KV-cache memory significantly. Therefore, the 128K context should not
be used as the normal setting on my 8 GB laptop.

gpt-oss-20b is much larger and is not suitable for my 8 GB laptop because its
Ollama size alone is around 14 GB.

For my scenario, memory requirements and licence permissions are both important.
A model should not be selected only because it has a small download size.
## 3.3 Context and Quantization Observation

I used my `vram_estimate.py` program to observe how context length and
quantization affect memory usage.

### Context Length Experiment

For the same 8B Q4_K_M model:

| Context Length | Weights (GB) | KV Cache (GB) | Total Memory (GB) |
|---:|---:|---:|---:|
| 4K | 4.56 | 0.64 | 5.72 |
| 8K | 4.56 | 1.28 | 6.42 |
| 32K | 4.56 | 5.12 | 10.65 |
| 128K | 4.56 | 20.48 | 27.54 |

The model weights stay the same when the context length changes. The KV cache
increases as the context length increases. Therefore, increasing the context
length increases the total memory requirement.

On my 8 GB laptop, 8K context is possible for an 8B Q4_K_M model but is
already fairly tight. A 32K or 128K context would exceed my 8 GB memory
budget.

### Quantization Experiment

For the same 8B model at 8K context:

| Quantization | Bytes per Parameter | Weights (GB) | Total Memory (GB) |
|---|---:|---:|---:|
| Q3_K_M | 0.43 | 3.44 | 5.19 |
| Q4_K_M | 0.57 | 4.56 | 6.42 |
| Q5_K_M | 0.68 | 5.44 | 7.39 |
| Q8_0 | 1.00 | 8.00 | 10.21 |
| FP16 | 2.00 | 16.00 | 19.01 |

The context experiment changes the KV-cache memory, while the quantization
experiment changes the model weight memory.

Q4_K_M is a useful balance for my scenario because it significantly reduces
memory compared with FP16 while keeping the estimated memory below 8 GB.

Lower quantization such as Q3_K_M uses less memory, but it may involve a
quality trade-off. Higher precision such as FP16 may provide better numerical
quality but requires much more memory.
## 3.4 Estimate vs Reality

I attempted to check a locally installed model using Ollama.

I ran:

```text
ollama list

However, Ollama was not installed or was not available in my PowerShell
environment, so I could not perform the `ollama ps` comparison on my own
machine.

### Local Model Check

| Item | Result |
|---|---|
| Ollama installed? | No |
| `ollama list` | Command not recognized |
| `ollama ps` | Not available |
| Local model checked | No local model |
| Memory estimate | Based on the Day 4 estimation formula |

Because I could not run a local model, I could not compare the estimated memory
with actual runtime memory on my machine.

The Day 4 formula is an estimate. Actual memory usage can differ depending on
the model architecture, context length, quantization and runtime.

Therefore, I use the memory estimate as a planning tool rather than treating it
as a guarantee of actual runtime memory.
## 3.5 Suitability Analysis

My scenario is a local college-fee assistant running on a laptop with 8 GB of
available memory.

For this scenario, memory usage is an important limitation. A very large model
or a full-precision model such as FP16 would not fit within my memory budget.

The 1.5B Q4_K_M configuration requires approximately 1.20 GB, so it fits
comfortably on my laptop. This makes it a practical choice for a simple
college-fee assistant.

The 8B Q4_K_M configuration requires approximately 6.42 GB at 8K context. It
can fit within 8 GB, but it is tight and leaves less memory for the operating
system and other applications.

Mistral 7B Instruct v0.3 is also a possible option because its estimated
memory requirement is lower than the 8B configurations I compared. However,
actual runtime memory should be checked before relying on it.

For my scenario, I would choose a smaller quantized model such as a 1.5B Q4
model because the task is relatively simple and does not require a very large
model.

I would also use a moderate context length instead of a very large context
because the KV cache increases as context length increases.

The licence is another important consideration. I would choose a model with a
licence that permits my intended use and would keep a record of the exact model
version, licence and source.

Therefore, my main choice is a small Q4-quantized model because it provides a
better balance between memory usage, simplicity and suitability for my
college-fee assistant.
## 3.6 Conclusion

For my local college-fee assistant, memory and licensing are both important
when selecting an AI model.

My memory calculations show that a 1.5B Q4_K_M model requires approximately
1.20 GB, so it fits comfortably within my 8 GB memory budget.

An 8B Q4_K_M model requires approximately 6.42 GB at 8K context. Although it
can fit within 8 GB, it is much tighter and leaves less memory for other
applications.

I also observed that increasing context length increases KV-cache memory, while
higher-precision models require more memory for their weights. Quantization
therefore provides an important way to reduce memory usage.

For my scenario, I recommend a small Q4-quantized model because the college-fee
assistant does not require a very large model. I would use a moderate context
length and avoid unnecessarily high precision.

I would also verify the exact model card and licence before using or
redistributing the model. Model size alone is not enough to decide whether a
model is suitable.

Overall, the best choice for my laptop is a small quantized model that fits
comfortably within the memory budget and has a licence that permits my intended
use.

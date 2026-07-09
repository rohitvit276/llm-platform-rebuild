# AI Model Server (llama.cpp)

This project runs a local AI inference server using **llama.cpp**, containerized with Docker. It exposes an **OpenAI-compatible API** to enable local LLM interaction.

Here is the reference repository. https://github.com/ggml-org/llama.cpp

## Architecture Overview

The server runs a local model inside a Docker container and exposes an HTTP API that follows the **OpenAI Chat Completions** contract.

## Prerequisites

- **Docker Desktop** installed and running.
- A **`.gguf` model file** (for example: `qwen2.5-0.5b-instruct-q4_k_m.gguf`).
- The Qwen2.5 model .gguf files can be downloaded from here - https://huggingface.co/Hugggme/Qwen2.5-0.5B-Instruct-Q4_K_M-GGUF/tree/main

## Setup and Running

1. Download the model and place it in your `./models` directory.
2. Launch the server using the command below (adjust the path to your local model folder):

```bash
docker run -d -p 8080:8080 -v "/path/to/your/models:/models" ghcr.io/ggml-org/llama.cpp:server --model "/models/qwen2.5-0.5b-instruct-q4_k_m.gguf" --host 0.0.0.0 --port 8080
```
```Powershell
docker run -p 8080:8080 -v "D:\projects\llm-platform-rebuild\models:/models" ghcr.io/ggml-org/llama.cpp:server --model "/models/qwen2.5-0.5b-instruct-q4_k_m.gguf" --host 0.0.0.0 --port 8080
```

## API Usage

The server implements the standard endpoint:

- `POST /v1/chat/completions`

## Testing the API

Create a file named `body.json`:

```json
{
  "model": "qwen2.5",
  "messages": [
    { "role": "user", "content": "Who is the prime minister of India?" }
  ]
}
```

Send the request using `curl`:

```bash
curl.exe -X POST http://localhost:8080/v1/chat/completions -H "Content-Type: application/json" -d "@body.json"
```

## Observability

- **Health check:** `GET http://localhost:8080/health`
- **Metrics:** `GET http://localhost:8080/metrics` (requires the `--metrics` flag at startup)

## What is GGUF?

**GGUF** stands for **GPT-Generated Unified Format**. It is a specialized binary file format designed to store large language models (LLMs) so they can run efficiently on consumer-grade hardware (such as laptops and desktops).

It was created by the **llama.cpp** project.

## What is llama.cpp?

At its core, **llama.cpp** is a high-performance software library for running large language models (LLMs)—such as **Llama, Qwen, and Mistral**—on standard consumer hardware, without requiring large cloud infrastructure.

It was created by **Georgi Gerganov** and has become a widely adopted standard for local and private AI inference.

## What is Q4_K_M?

## Understanding Q4_K_M
**Q4** The models weight has been compressed to 4 bit precision instead of 16 bit precision. This helps reduce file size and memory requirements.
**K_M (K-Quant, Medium)**: This is a specific, modern strategy for compressing models. It is loved by local users because of compressed and small sizes.

**Q4_K_M** is a widely used quantization format in the local LLM ecosystem, specifically designed for use with the **GGUF** file format and the **llama.cpp** runtime.
In simple terms, it reduces model size and memory usage while preserving reasonable quality and speed.

The .gguf file downloaded for the model **qwen2.5-0.5b-instruct-q4_k_m.gguf** is around 380 MBs in size whereas a at FP16 the model sizes are approximately 1GB, so there is a clear 1/3rd size file. 

## Token Usage

I observed that it uses about **35–50 tokens per second**.

## What Surprised Me

The model hallucinates frequently and can return different (and sometimes incorrect) answers to the same question when asked again after a few minutes.

It also tends to misunderstand queries instead of asking clarifying questions. Example:

### Query

**How large is India compared to the USA?**

### Observed incorrect behavior

The model responded with a population-based and incorrect comparison, including inconsistent numbers and calculation formatting.

## Why might it run faster on host vs container?


- **Host (direct):** ~11.9 tokens/sec  
- **Container:** ~40–49 tokens/sec

So, when I ran the llama.cpp directly on host through llama CLI, it was different model named **gemma-3-1b-it-GGUF**. 
The Model which I built on docker and ran it was **Hugggme/Qwen2.5-0.5B-Instruct-Q4_K_M-GGUF**. The difference between these models is that the gemma-3 is 1B model or the 1 Billon model while the Qwen2.5-05B is a 0.5B or 0.5Billion Model, so clearly the gemma-3 is twice more resources in terms of knowledge compared to the Qwen2.5. Hence Qwen2.5 provides faster response comapred to the gemma-3b, because for every question gemma-3b has to look into a twice as wider set of items comapared to the Qwen2.5. 

Hence, because of faster movement the 0.5B model will generate more tokens/second and the 1B modle will produce lesser as observed above.


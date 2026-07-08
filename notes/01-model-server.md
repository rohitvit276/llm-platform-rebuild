# AI Model Server (llama.cpp)

This project runs a local AI inference server using **llama.cpp**, containerized with Docker. It exposes an **OpenAI-compatible API** to enable local LLM interaction.

## Architecture Overview

The server runs a local model inside a Docker container and exposes an HTTP API that follows the **OpenAI Chat Completions** contract.

## Prerequisites

- **Docker Desktop** installed and running.
- A **`.gguf` model file** (for example: `qwen2.5-0.5b-instruct-q4_k_m.gguf`).

## Setup and Running

1. Download the model and place it in your `./models` directory.
2. Launch the server using the command below (adjust the path to your local model folder):

```bash
docker run -d -p 8080:8080 -v "/path/to/your/models:/models" ghcr.io/ggml-org/llama.cpp:server --model "/models/qwen2.5-0.5b-instruct-q4_k_m.gguf" --host 0.0.0.0 --port 8080
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

**Q4_K_M** is a widely used quantization format in the local LLM ecosystem, specifically designed for use with the **GGUF** file format and the **llama.cpp** runtime.

In simple terms, it reduces model size and memory usage while preserving reasonable quality and speed.

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

You noted this behavior:

- **Host (direct):** ~11.9 tokens/sec  
- **Container:** ~40–49 tokens/sec

That result is unusual, because containerized workloads are often similar or slightly slower than host execution unless configuration differs.

Possible reasons include:

- Different runtime flags between host and container runs.
- Different CPU/GPU backends being used.
- Threading configuration differences.
- Docker resource limits or affinity settings.
- Model loading/caching differences.

In short, performance differences are usually due to **configuration mismatch**, not Docker alone.

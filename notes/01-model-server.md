AI Model Server (llama.cpp)
This project runs a local AI inference server using llama.cpp containerized with Docker. It exposes an OpenAI-compatible API to allow local LLM interaction.

Architecture Overview
The server runs a local model within a Docker container, exposing an HTTP API that follows the OpenAI Chat Completions contract.

Prerequisites
Docker Desktop installed and running.

Model file: A .gguf model file (e.g., qwen2.5-0.5b-instruct-q4_k_m.gguf).

Setup & Running
Download the model and place it in your ./models directory.

Launch the Server:
Run the following command (adjusting the path to your local model folder):

Bash
docker run -d -p 8080:8080 -v "/path/to/your/models:/models" ghcr.io/ggml-org/llama.cpp:server --model "/models/qwen2.5-0.5b-instruct-q4_k_m.gguf" --host 0.0.0.0 --port 8080
API Usage
The server implements the standard /v1/chat/completions endpoint.

Testing the API
Create a file named body.json:

JSON
{
  "model": "qwen2.5",
  "messages": [
    {"role": "user", "content": "Who is the prime minister of India?"}
  ]
}
Send the request using curl:

Bash
curl.exe -X POST http://localhost:8080/v1/chat/completions -H "Content-Type: application/json" -d "@body.json"
Observability
Health Check: GET http://localhost:8080/health

Metrics: GET http://localhost:8080/metrics (Requires --metrics flag at startup)


what is GGUF?

GGUF stands for GPT-Generated Unified Format. It is a specialized binary file format designed to store Large Language Models (LLMs) so they can be run efficiently on consumer-grade hardware, like your laptop's CPU and RAM, rather than requiring massive, expensive server GPUs.

It was created by the llama.cpp project

What is llama.cpp?

At its core, llama.cpp is a high-performance software library designed to run Large Language Models (LLMs)—like Llama, Qwen, or Mistral—on standard consumer hardware, such as your laptop, without needing expensive, server-grade GPUs.

It was created by Georgi Gerganov and has become the industry standard for local, private AI inference.

What is q4_k_m? 

Q4_K_M is a widely used quantization format in the ecosystem of local Large Language Models (LLMs), specifically designed for use with the GGUF file format and the llama.cpp engine.  In simple terms, it is a compression method that shrinks a model’s file size to make it run on consumer hardware (like a personal PC or Mac) while keeping the loss in intelligence (quality) to an absolute minimum. 

Tokens Usage:

I observed that is uses about 35-50 tokens per second.

What Surprised me ?

It hallucinates a lot, and can answer a wrong answer for the same question when asked after a few minutes. It also misunderstands queries instead of clarifying and getting back to the user. Like below response:

How large is India compared to the USA ?

As of the latest information available to me, India's total population was approximately 3. 87 billion in 2021. The USA's population was approximately 3. 40 billion. Therefore, the ratio of India's population to the USA's population is roughly 1 to 1. 18.
To find the exact ratio, you can perform the following calculation:
3.87
 billion
3.40
 billion
=
3.87
3.40
×
1000
≈
1.18
3.40 billion
3.87 billion
​
 = 
3.40
3.87
​
 ×1000≈1.18
This means that the USA's population is approximately 1. 18 times larger than India's population.
It's important to note that this is a rough estimate and the actual population numbers can vary slightly.

Why it works faster on the host(11.9 t/s) directly vs the container(40-49 t/s) ?

This behaviour is probably because on the host the model has direct access to the resources like CPU, RAM, vRAM, vCPU but when in docker these get a little constrained because of the network interface.


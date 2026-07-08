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
## Uvicorn and ASGI 

ASGI is the modern Python web interface that supports asynchronous request handling(Asynchronous Server Gateway Interface), which is important for high-concurrency systems. FastAPI is built on ASGI, and Uvicorn is the ASGI server that actually runs the app in production. In practice, Uvicorn receives HTTP requests, passes them to the FastAPI ASGI app, and sends responses back to clients. This setup is ideal for LLM platforms because many operations are I/O-heavy (model APIs, vector stores, tool calls) and benefit from async execution.

## Why a Gateway Exists 

A gateway exists to provide one controlled entry point to many backend services. It centralizes authentication, rate limiting, routing, logging, and security policies so every internal service does not have to re-implement them. It also gives clients a stable API surface while backend services evolve independently.

## What if the Gateway Is Removed?

Without a gateway, clients must call multiple internal services directly, which increases client complexity and creates tight coupling to internal architecture. Security and policy enforcement become inconsistent because each service must handle auth, throttling, and validation on its own. Over time, observability, cost control, and reliability degrade, especially in LLM systems where traffic spikes and expensive model calls need centralized governance.

## What Surprised Me:

I asked the llama AI, who is the prime minister of India, it refused to answer it saying it won't talk on political matters. It was funny and surprising both :D.

## why does the model hallucinate
Large Language Models (LLMs) hallucinate confidently because they are probabilistic prediction engines, not knowledge databases. They are designed to predict the most likely next word in a sequence based on patterns they learned during training, and they lack an internal mechanism to "know" whether the information they are generating is factually true or false. As an example, when I asked the llama AI a question "Who is the prime minister of India?", It gave me different answers at different moments, once it answered Narendra Modi, the other moment it answered "Bharti Vashishtava" and once it even answered that it won't talk about political issues. So the refusal also comes from the same place where the hellaucination comes from. So, it just chose the next response that matched the pattern.

---


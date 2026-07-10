## Uvicorn and ASGI (How FastAPI Runs)

### What is ASGI?
**ASGI (Asynchronous Server Gateway Interface)** is a standard interface between Python web applications and web servers.  
It is the modern alternative to WSGI and is designed for **async/concurrent** workloads.

In simple terms:
- The app (FastAPI/Starlette) speaks **ASGI**
- The server (Uvicorn) understands ASGI and runs my app

---

### What is Uvicorn?
**Uvicorn** is a lightweight, high-performance **ASGI server** for Python.

Uvicorn is responsible for:
- Accepting incoming HTTP connections
- Translating requests into ASGI events
- Passing those events to your FastAPI app
- Returning the app’s response back to the client

So:
- **FastAPI = application framework**
- **ASGI = communication contract**
- **Uvicorn = runtime server that executes the ASGI app**

---

### Why this matters in an LLM platform
LLM systems often involve:
- Many concurrent requests
- Streaming responses
- I/O-heavy calls (vector DBs, model APIs, tools)

ASGI + Uvicorn are a good fit because they handle async workloads efficiently and support modern patterns like streaming and long-lived connections.

---

## Why an API Gateway Exists

An **API Gateway** is the single entry point in front of backend services (auth, orchestration, model routing, retrieval, etc.).

Think of it as a traffic controller for your platform.

### Core reasons to have a gateway
1. **Single public entry point**  
   Clients talk to one endpoint instead of many internal services.

2. **Centralized authentication and authorization**  
   Enforce API keys/JWT, tenant rules, and role checks in one place.

3. **Rate limiting and abuse protection**  
   Prevent spam, overload, and accidental cost explosions.

4. **Request routing and service composition**  
   Send each request to the correct internal service/model pipeline.

5. **Observability and logging**  
   Unified metrics, tracing, and request logs across the platform.

6. **Security boundary**  
   Keep internal services private; expose only controlled public surfaces.

7. **Policy enforcement**  
   Apply quotas, payload limits, CORS, and validation consistently.

---

## What happens if the gateway is not there?

If you remove the gateway, the system can still work in small/simple setups, but operational and security risks grow quickly.

### Likely consequences
1. **Clients must call multiple services directly**  
   More client complexity and tighter coupling to internal architecture.

2. **Inconsistent auth and policies**  
   Every service must re-implement auth, rate limits, and validation (easy to get wrong).

3. **Higher attack surface**  
   More public endpoints means more places to misconfigure or exploit.

4. **Harder monitoring and debugging**  
   Logs/metrics are fragmented across services with no unified request path.

5. **No central throttling/cost control**  
   Expensive LLM endpoints are easier to abuse or accidentally overload.

6. **More duplicated code and slower iteration**  
   Common cross-cutting concerns are repeated in each service.

7. **Breaking changes become riskier**  
   Internal service changes can leak to clients because there’s no stable façade layer.

## What Surprised Me:

The api gateway answers on port 9000, post configuration but the LLM app directly answers on port 8080.

## why does the model hallucinate
Large Language Models (LLMs) hallucinate confidently because they are probabilistic prediction engines, not knowledge databases. They are designed to predict the most likely next word in a sequence based on patterns they learned during training, and they lack an internal mechanism to "know" whether the information they are generating is factually true or false.

---

## Practical summary
- **Uvicorn + ASGI** power how your FastAPI services run efficiently.
- **Gateway** provides control, security, and consistency at platform level.
- Without a gateway, complexity shifts to every service and every client, which usually hurts scalability and reliability.

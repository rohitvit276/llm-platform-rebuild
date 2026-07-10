from fastapi import FastAPI, Response, Request
import httpx

app = FastAPI()

# UPSTREAM_URL is strictly the base address
UPSTREAM_URL = "http://localhost:8080"

@app.get("/health")
async def readiness_check():
    """
    Readiness probe: Returns 200 only when the upstream model is fully loaded.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{UPSTREAM_URL}/health", timeout=2.0)
            
            if response.status_code == 200:
                return {"status": "ready", "upstream": "connected"}
            else:
                return Response(
                    content='{"status": "unhealthy", "reason": "upstream not ready"}',
                    status_code=503,
                    media_type="application/json"
                )
                
    except (httpx.ConnectError, httpx.TimeoutException):
        return Response(
            content='{"status": "unhealthy", "reason": "upstream unreachable"}',
            status_code=503,
            media_type="application/json"
        )

@app.post("/v1/chat/completions")
async def chat_proxy(request: Request):
    # Read the raw body
    body = await request.body()
    
    async with httpx.AsyncClient() as client:
        try:
            # Explicitly target the full endpoint
            response = await client.post(
                f"{UPSTREAM_URL}/v1/chat/completions",
                content=body,
                headers={"Content-Type": "application/json"},
                timeout=60.0
            )
            
            return Response(
                content=response.content,
                status_code=response.status_code,
                media_type="application/json"
            )
            
        except httpx.ConnectError:
            return Response(
                content='{"error": "upstream server unreachable"}',
                status_code=502,
                media_type="application/json"
            )
        except httpx.TimeoutException:
            return Response(
                content='{"error": "upstream request timed out"}',
                status_code=504,
                media_type="application/json"
            )
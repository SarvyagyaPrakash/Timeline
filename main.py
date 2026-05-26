from datetime import datetime, timezone
import json
import sys
from fastapi import FastAPI, Request

# =====================================================================
# FastAPI Application Metadata
# =====================================================================
# We initialize the FastAPI application and configure the metadata 
# specified in the project requirements.
app = FastAPI(
    title="Timeline Orchestra Backend",
    description="Infrastructure layer for Timeline Orchestra",
    version="0.1.0"
)

# =====================================================================
# Shared Infrastructure Helpers
# =====================================================================
def log_webhook_payload(payload: dict) -> None:
    """
    Helper function to print incoming webhook payloads to the terminal.
    It formats and logs a visible separator, receipt message, current ISO 8601
    UTC timestamp, and pretty-printed JSON payload.
    """
    timestamp = datetime.now(timezone.utc).isoformat()
    separator = "=" * 60
    
    print(separator)
    print("Incoming webhook received!")
    print(f"Timestamp: {timestamp}")
    print("Payload:")
    print(json.dumps(payload, indent=2))
    print(separator)
    sys.stdout.flush()


# =====================================================================
# Route 1 — Health Check
# =====================================================================
# - WHAT IT DOES: 
#   This route serves as a quick sanity check to verify that the backend 
#   service is up, running, and accessible on the network.
# - WHY IT RETURNS 200: 
#   An HTTP status code 200 (OK) indicates that the request was successful 
#   and the server is functioning properly. Returning 200 is standard practice
#   for health check endpoints so automated load balancers or uptime monitors
#   know the container/service is healthy.
# - WHAT "async" MEANS: 
#   The "async" keyword before "def" tells Python that this function is a 
#   coroutine. In simple terms, it means the server can temporarily pause 
#   executing this specific request if it needs to wait for something else
#   (like database queries or network requests) and handle other incoming 
#   requests in the meantime. This prevents the server from blocking.
# =====================================================================
@app.get("/")
async def health_check():
    return "Orchestra Backend Set by Sarvyagya"


# =====================================================================
# Route 2 — Webhook Receiver
# =====================================================================
# - WHAT IT DOES:
#   This route receives incoming HTTP POST requests containing webhook payloads 
#   from external platforms, parses the body, logs the pretty-printed content 
#   to the terminal, and acknowledges receipt.
# - WHY IT RETURNS 200:
#   Typically, HTTP POST requests might return HTTP 201 (Created) when 
#   generating database resources. However, webhooks from external systems
#   require a rapid, standard HTTP 200 OK acknowledgment to indicate that the 
#   payload was successfully received and ingested. If a receiver returned a
#   different code or delayed acknowledgment, the external platform might 
#   mistakenly think the transmission failed and retry indefinitely.
# - WHAT "async" MEANS:
#   The "async" keyword allows the endpoint to yield control while reading
#   the request body from the network, letting FastAPI handle other clients 
#   concurrently without blocking the main event loop.
# - WHAT THE "Request" OBJECT IS:
#   The "Request" object is a FastAPI/Starlette utility that represents the 
#   raw incoming HTTP request. It contains all metadata about the request, 
#   including HTTP headers, query parameters, client IP address, cookies, and 
#   allows us to asynchronously read the raw binary body and parse it as JSON
#   using "await request.json()".
# =====================================================================
@app.post("/webhook")
async def receive_webhook(request: Request):
    # Retrieve the incoming JSON body dynamically using the Request object
    payload = await request.json()
    
    # Print the formatted log output to the terminal
    log_webhook_payload(payload)
    
    # Return receipt confirmation JSON with HTTP 200 OK status
    return {
        "received": True,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# =====================================================================
# Route 3 — Webhook Simulator (for internal testing)
# =====================================================================
# - WHAT IT DOES:
#   This route allows developers or internal tools to simulate receiving an 
#   incoming webhook. It takes the payload, runs it through the same logging 
#   logic as Route 2, and echoes back the simulated payload along with a timestamp.
# - WHY IT RETURNS 200:
#   Returning 200 OK indicates that the simulation successfully processed 
#   and registered the event payload in the server log.
# - WHAT "async" MEANS:
#   Like the webhook receiver, it prevents blocking of the single-threaded 
#   event loop during asynchronous body reading operations.
# - WHAT THE "Request" OBJECT IS:
#   Here, the "Request" object is again utilized to dynamically read and parse
#   the JSON payload from the request body without forcing a rigid database/Pydantic
#   schema, allowing us to simulate any format of incoming webhook.
# =====================================================================
@app.post("/test/simulate-webhook")
async def simulate_webhook(request: Request):
    # Parse the simulation body using the Request object
    payload = await request.json()
    
    # Log the payload using the same helper as Route 2
    log_webhook_payload(payload)
    
    # Return simulation success body with the echoed payload and timestamp
    return {
        "simulated": True,
        "payload_received": payload,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

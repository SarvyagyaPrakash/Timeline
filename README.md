# Timeline Orchestra Backend 🎻⏳

Infrastructure layer for **Timeline Orchestra**, a collaborative project management tool. This backend provides platform-specific webhook ingestion for **GitHub**, **Discord**, and **Figma**, a mock tasks API for frontend development, and an internal simulation system for testing webhook workflows.

---

## 🚀 Quick Start & Environment Setup

Follow these steps to set up, activate, and run the Python environment on your local macOS machine.

### 1. Set Up the Virtual Environment
Navigate to the project root and create a virtual environment named `venv`:
```bash
# Navigate to the backend directory (if not already inside)
cd Timeline

# Create a fresh Python virtual environment
python3 -m venv venv
```

### 2. Activate the Virtual Environment
Before installing dependencies or running the server, activate the environment:
```bash
source venv/bin/activate
```
*Note: Once activated, your terminal prompt will be prefixed with `(venv)`.*

### 3. Install Requirements
Install all framework and server dependencies using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

---

## ⚙️ Running the Server

Start the local development server utilizing **Uvicorn** with hot-reload enabled:
```bash
uvicorn main:app --reload
```
The server will boot up and bind to `http://127.0.0.1:8000`. You can access the interactive Swagger API documentation at:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

## 🛜 Exposing the Server Externally with Ngrok

To receive live webhooks from external systems or collaborative teammates, you must expose your local port `8000` via **ngrok**.

### Step-by-Step Manual Guide:
1. Ensure `ngrok` is installed on your machine (e.g. `brew install ngrok`).
2. Run the tunnel command in a separate terminal window:
   ```bash
   ngrok http 8000
   ```
3. Copy the generated **Forwarding URL** (e.g., `https://xxxx-xx-xx-xx.ngrok-free.app`).
4. > [!IMPORTANT]
   > **Note for Collaborative Integration:**
   > You **MUST** share this ngrok URL with **Member 4** so they can configure external event sources to route payloads to your server.

---

## 📡 API Endpoints & Routes Documentation

### 1. Health Check
* **Method:** `GET`
* **Path:** `/`
* **Purpose:** Evaluates overall API availability.
* **HTTP Status Code:** `200 OK`
* **Response:**
  ```
  "Orchestra Backend Set by Sarvyagya"
  ```

---

### 2. Generic Webhook Receiver *(backward-compatible, Stage 1)*
* **Method:** `POST`
* **Path:** `/webhook`
* **Purpose:** Catch-all webhook endpoint kept for backward compatibility. Logs payloads tagged as `GENERIC` to the terminal.
* **HTTP Status Code:** `200 OK` (always — prevents remote retry storms)
* **Payload Format:** Any valid JSON body.
* **Response Payload Example:**
  ```json
  {
    "received": true,
    "timestamp": "2026-05-29T09:29:30.987654+00:00"
  }
  ```

---

### 3. GitHub Webhook Receiver *(Stage 2)*
* **Method:** `POST`
* **Path:** `/webhook/github`
* **Purpose:** Dedicated endpoint for GitHub events (push, pull_request, issues, etc.). GitHub includes an `X-GitHub-Event` header identifying the event type. Payloads are logged tagged as `GITHUB`.
* **HTTP Status Code:** `200 OK`
* **Response Payload Example:**
  ```json
  {
    "received": true,
    "platform": "github",
    "timestamp": "2026-05-29T09:30:00.000000+00:00"
  }
  ```

---

### 4. Discord Webhook Receiver *(Stage 2)*
* **Method:** `POST`
* **Path:** `/webhook/discord`
* **Purpose:** Dedicated endpoint for Discord events (messages, bot commands, member joins/leaves). Handles the **Discord verification handshake** automatically — when Discord first registers the URL, it sends `{ "type": 1 }` and expects `{ "type": 1 }` in return.
* **HTTP Status Code:** `200 OK`
* **Verification Handshake Response:**
  ```json
  { "type": 1 }
  ```
* **Normal Event Response:**
  ```json
  {
    "received": true,
    "platform": "discord",
    "timestamp": "2026-05-29T09:30:00.000000+00:00"
  }
  ```

---

### 5. Figma Webhook Receiver *(Stage 2)*
* **Method:** `POST`
* **Path:** `/webhook/figma`
* **Purpose:** Dedicated endpoint for Figma design events. Figma fires this when a designer updates a file, publishes a library, or adds a comment. Payloads are logged tagged as `FIGMA`.
* **Common Figma `event_type` values:**
  | Event Type | Meaning |
  |---|---|
  | `FILE_UPDATE` | A file was edited |
  | `FILE_COMMENT` | A comment was added to a design |
  | `LIBRARY_PUBLISH` | A shared design library was updated |
* **HTTP Status Code:** `200 OK`
* **Response Payload Example:**
  ```json
  {
    "received": true,
    "platform": "figma",
    "timestamp": "2026-05-29T09:30:00.000000+00:00"
  }
  ```

---

### 6. Mock Tasks Endpoint *(Stage 2)*
* **Method:** `GET`
* **Path:** `/tasks`
* **Purpose:** Returns hardcoded sample task data so the frontend team can build and test the UI without waiting for the real database. The JSON shape exactly matches what will be returned once Neo4j is connected — frontend code won't need to change.
* **HTTP Status Code:** `200 OK`
* **Task Field Reference:**

  | Field | Type | Description |
  |---|---|---|
  | `id` | string | Unique task identifier |
  | `title` | string | Short task name |
  | `description` | string | Full task details |
  | `status` | string | `"todo"` / `"in_progress"` / `"completed"` |
  | `assigned_to` | string | Team member responsible |
  | `platform` | string | Source platform: `github` / `figma` / `discord` |
  | `priority` | string | `"high"` / `"medium"` / `"low"` |
  | `created_at` | string | ISO 8601 UTC timestamp |
  | `updated_at` | string | ISO 8601 UTC timestamp |

* **Response Payload Example:**
  ```json
  {
    "total": 8,
    "tasks": [
      {
        "id": "task_001",
        "title": "Set up Neo4j database schema",
        "status": "completed",
        "assigned_to": "Member 2 — Knowledge Graph Engineer",
        "platform": "github",
        "priority": "high",
        ...
      }
    ]
  }
  ```

---

### 7. Webhook Simulator *(Stage 1, kept)*
* **Method:** `POST`
* **Path:** `/test/simulate-webhook`
* **Purpose:** Simulates receiving an incoming webhook internally. Runs through the identical logging routine as the real receivers and echoes the parsed content back. Useful for smoke-testing the pipeline without an external system.
* **HTTP Status Code:** `200 OK`
* **Payload Format:** Any valid JSON body.
* **Response Payload Example:**
  ```json
  {
    "simulated": true,
    "payload_received": {
      "event": "project.created",
      "data": {
        "id": 101,
        "name": "Q2 Launch Campaign"
      }
    },
    "timestamp": "2026-05-29T09:30:15.555555+00:00"
  }
  ```

---

## 🔧 Shared Infrastructure Helper

All webhook routes use the shared `log_webhook_payload(platform, payload)` helper:

```
============================================================
Incoming webhook received!
Platform  : DISCORD
Timestamp : 2026-05-29T09:29:30.987654+00:00
Payload:
{
  "type": 0,
  "content": "Hello from Discord!"
}
============================================================
```

The `Platform` field was added in Stage 2 so you can immediately identify the source of any event in the terminal.

---

## 🧪 Testing with Hoppscotch

You can test all routes using **[Hoppscotch](https://hoppscotch.io)**, Postman, or Insomnia.

### `GET /` — Health Check
1. Set method to `GET`.
2. Enter URL: `http://127.0.0.1:8000/`
3. Press **Send** — expect a `200 OK` response.

### `POST /webhook/github` — GitHub Events
1. Set method to `POST`.
2. Enter URL: `http://127.0.0.1:8000/webhook/github`
3. Body (JSON):
   ```json
   {
     "ref": "refs/heads/main",
     "commits": [{ "message": "Add Figma webhook endpoint" }],
     "pusher": { "name": "sarvyagya" }
   }
   ```
4. Click **Send** — expect `"platform": "github"` in the response.

### `POST /webhook/discord` — Discord Events
1. Set method to `POST`.
2. Enter URL: `http://127.0.0.1:8000/webhook/discord`
3. Body (JSON) — normal event:
   ```json
   {
     "type": 0,
     "content": "Task completed!",
     "author": { "username": "sarvyagya" }
   }
   ```
4. To test the **verification handshake**, send `{ "type": 1 }` — you should get `{ "type": 1 }` back.

### `POST /webhook/figma` — Figma Events
1. Set method to `POST`.
2. Enter URL: `http://127.0.0.1:8000/webhook/figma`
3. Body (JSON):
   ```json
   {
     "event_type": "FILE_UPDATE",
     "file_key": "abc123",
     "file_name": "Timeline — UI Kit"
   }
   ```
4. Click **Send** — expect `"platform": "figma"` in the response.

### `GET /tasks` — Mock Tasks
1. Set method to `GET`.
2. Enter URL: `http://127.0.0.1:8000/tasks`
3. Click **Send** — expect a JSON object with `"total": 8` and the full task list.

### `POST /test/simulate-webhook` — Internal Simulation
1. Set method to `POST`.
2. Enter URL: `http://127.0.0.1:8000/test/simulate-webhook`
3. Paste any JSON payload in the Body tab.
4. Click **Send** — expect `"simulated": true` and your payload echoed back in `"payload_received"`.

---

## 📋 Route Summary

| Method | Path | Stage | Description |
|---|---|---|---|
| `GET` | `/` | 1 | Health check |
| `POST` | `/webhook` | 1 | Generic catch-all webhook receiver |
| `POST` | `/webhook/github` | 2 | GitHub-specific webhook receiver |
| `POST` | `/webhook/discord` | 2 | Discord webhook receiver (with verification handshake) |
| `POST` | `/webhook/figma` | 2 | Figma design event receiver |
| `GET` | `/tasks` | 2 | Mock task list for frontend development |
| `POST` | `/test/simulate-webhook` | 1 | Internal webhook simulator |

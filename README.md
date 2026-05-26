# Timeline Orchestra Backend 🎻⏳ (Stage 1)

Infrastructure layer for **Timeline Orchestra**, a collaborative project management tool. This backend provides the core health checks, a robust webhook ingestion pipeline, and an internal simulation system for testing webhook workflows.

---

## 🚀 Quick Start & Environment Setup

Follow these steps to set up, activate, and run the Python environment on your local macOS machine.

### 1. Set Up the Virtual Environment
Navigate to the project root and create a virtual environment named `venv`:
```bash
# Navigate to the backend directory (if not already inside)
cd timeline-orchestra-backend

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
* **Response Payload Example:**
  ```json
  {
    "status": "online",
    "message": "Timeline Orchestra Backend is active and running.",
    "member": "Member 3 — Infrastructure Engineer",
    "stage": "Stage 1 — Boilerplate",
    "timestamp": "2026-05-26T09:29:28.123456+00:00"
  }
  ```

### 2. Webhook Receiver
* **Method:** `POST`
* **Path:** `/webhook`
* **Purpose:** Ingests external webhook payloads, parses raw json, and pretty-prints formatted logs directly to the server shell.
* **HTTP Status Code:** `200 OK` (Always returned to prevent remote retry loop-storms).
* **Payload Format:** Accepts any valid JSON body.
* **Response Payload Example:**
  ```json
  {
    "received": true,
    "timestamp": "2026-05-26T09:29:30.987654+00:00"
  }
  ```

### 3. Webhook Simulator
* **Method:** `POST`
* **Path:** `/test/simulate-webhook`
* **Purpose:** Simulates receiving an incoming webhook internally. Triggers the identical logging routine as `/webhook` and echoes the parsed content back in the JSON body.
* **HTTP Status Code:** `200 OK`
* **Payload Format:** Accepts any valid JSON body.
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
    "timestamp": "2026-05-26T09:30:15.555555+00:00"
  }
  ```

---

## 🧪 Testing with Hoppscotch

You can test all routes by importing them into **[Hoppscotch](https://hoppscotch.io)** (or Postman/Insomnia):

### Testing `GET /` (Health Check)
1. In Hoppscotch, set the method dropdown to `GET`.
2. Enter your local URL: `http://127.0.0.1:8000/` or your ngrok URL `https://<your-subdomain>.ngrok-free.app/`.
3. Press **Send**. You should see the `200 OK` status and the JSON object confirming the status is `"online"`.

### Testing `POST /webhook` (Webhook Ingestion)
1. In Hoppscotch, set the method dropdown to `POST`.
2. Enter the URL: `http://127.0.0.1:8000/webhook`.
3. Go to the **Body** tab, select **JSON**, and paste a test payload:
   ```json
   {
     "event": "task.completed",
     "actor": "sarvyagya",
     "timestamp": "2026-05-26T14:58:05Z",
     "details": {
       "task_id": "orchestra-109",
       "title": "Complete Stage 1 Boilerplate"
     }
   }
   ```
4. Click **Send**.
5. Observe the response containing `"received": true`.
6. Go back to your terminal window where Uvicorn is running. You will see a beautiful terminal block containing:
   ```
   ============================================================
   Incoming webhook received!
   Timestamp: 2026-05-26T09:29:30.987654+00:00
   Payload:
   {
     "event": "task.completed",
     "actor": "sarvyagya",
     "timestamp": "2026-05-26T14:58:05Z",
     "details": {
       "task_id": "orchestra-109",
       "title": "Complete Stage 1 Boilerplate"
     }
   }
   ============================================================
   ```

### Testing `POST /test/simulate-webhook` (Simulation)
1. Set the method to `POST`.
2. Enter the URL: `http://127.0.0.1:8000/test/simulate-webhook`.
3. Paste a test payload in the **Body** (JSON) tab.
4. Click **Send** and verify you get an echoed response showing `"simulated": true` and your payload inside `"payload_received"`.

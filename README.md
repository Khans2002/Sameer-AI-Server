# SAMEER AI - WebServer Backend
**Secure Intelligence Gateway**

> **Developed by:** Gooty Mohammed Sameer Khan  
> **Role:** Host Server & API Bridge for Sameer AI Ecosystem

---

## 🛡️ Security & Strategy

This is not just a simple web server; it is the **Gateway** that protects and serves the Sameer AI Core.

### 1. The "Nuclear Firewall"
Because the underlying AI models (like Llama-3) are trained on general internet data, they can affect specific identities or "hallucinate" corporate origins (e.g., claiming to be from OpenAI).
*   **Strategy**: We implement a "Nuclear Firewall" interceptor in `server.py` that scans every user prompt and model response.
*   **Function**: It strictly enforces the "Sameer AI" identity, blocking any mention of external corporate entities or training data, ensuring the system remains true to its specific developer: **Gooty Mohammed Sameer Khan**.

### 2. The Fuse System (`core/fuse.py`)
To prevent system crashes on consumer hardware:
*   **Strategy**: A virtual "Fuse" monitors CPU and RAM usage in real-time.
*   **Action**: If the system load exceeds safety thresholds (e.g., 90% RAM), the "Fuse Blows", instantly rejecting new API requests with a 503 error until the system cools down. This guarantees the host machine never freezes.

---

## 🤖 AI Integration (Ruma & Monika)

The server acts as the hub for specialized agents:
1.  **Ruma (Vision)**: The server routes `/imagine` requests to the **Ruma Agent**, which generates images and serves them via the `/gallery` static mount.
2.  **Monika (Code)**: Code generation requests (`/monika`) are routed to the **Monika Agent** for high-precision logic synthesis.

---

## 🚀 Deployment

### Prerequisites
*   FastAPI & Uvicorn
*   Cloudflared (for secure tunneling)

### Run Command
```bash
./run_server.sh
```

---
*Verified Production Build - v1.0*

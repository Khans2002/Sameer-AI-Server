# Developer Notes: Sameer AI Web Server

## Technology Stack

### 1. Backend Core
- **Language**: Python 3.10+
- **Framework**: FastAPI (High-performance, async web framework)
- **Server**: Uvicorn (ASGI Server)
- **Key Libraries**:
    - `pydantic`: Data validation and settings management.
    - `psutil`: Real-time system monitoring (CPU/RAM Fuse).
    - `requests` / `httpx`: Internal API communication.
    - `jinja2`: Server-side template rendering.

### 2. Frontend Interface
- **Languages**: 
    - **HTML5**: Semantic structure.
    - **CSS3**: Custom "Glassmorphism" design system (Neon/Dark UI) without external frameworks.
    - **JavaScript (ES6+)**: Vanilla JS for async API calls, dynamic DOM updates, and agent switching logic.
- **Design Philosophy**: Minimalist, futuristic, responsive.

### 3. Infrastructure & Deployment
- **Scripting**: Bash (`.sh`) for setup, automation, and process management.
- **Tunneling**: Cloudflare Tunnel (`cloudflared`) for secure public exposure without port forwarding.
- **Environment**: Python Virtual Environment (`venv`) for dependency isolation.

### 4. AI Integration Layers
- **Ollama**: Local LLM interfacing via HTTP API (Llama 3.2).
- **Ruma Agent**: Custom Python-based Stable Diffusion integration (CPU-optimized).
- **Monika Agent**: Logic/Code generation integration.

## Directory Structure
- `server.py`: Main application entry point and logic.
- `static/`: CSS and JavaScript assets.
- `templates/`: HTML Jinja2 templates.
- `venv/`: Local Python dependencies.
- `run_server.sh`: Orchestration script.

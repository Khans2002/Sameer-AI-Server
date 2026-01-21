
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from core.config import *
from core.fuse import fuse
from core.security import check_auth, login_user, check_rate_limit
import uvicorn
import sys
import os
import httpx
import asyncio
import datetime

# --- AI CORE INTEGRATION ---
# Add Core System to Path
CORE_PATH = "/Volumes/Dr.Khans/Sameer Khan LocalAI /SAMEER_AI_System_v7"
sys.path.append(CORE_PATH)

try:
    from Agents.Ruma.Core.Ruma_Core import RumaAgent
    from Agents.Monika.Monika_Agent import MonikaAgent
    from MCP_Server.utils import identity
    print("✅ AI Core Logic Imported Successfully.")
except ImportError as e:
    print(f"❌ Critical Error Importing AI Core: {e}")
    # We will continue so the server doesn't crash, but AI config will be partially broken
    identity = None

# Initialize Agents
try:
    ruma_agent = RumaAgent()
    monika_agent = MonikaAgent()
    print("✅ Ruma & Monika Agents Initialized.")
except Exception as e:
    print(f"⚠️ Agent Initialization Warning: {e}")
    ruma_agent = None
    monika_agent = None

# --- APP SETUP ---
app = FastAPI(title="Sameer AI Server", version="1.0")

# Mount Static & Templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory="static"), name="static")

# Mount Ruma Gallery (Read-Only access to generated images)
RUMA_GALLERY = "/Volumes/Dr.Khans/Sameer Khan LocalAI /Ruma Agent Gallery"
if not os.path.exists(RUMA_GALLERY):
    os.makedirs(RUMA_GALLERY)
app.mount("/gallery", StaticFiles(directory=RUMA_GALLERY), name="gallery")

templates = Jinja2Templates(directory="templates")

# --- MIDDLEWARE: FUSE CHECK ---
@app.middleware("http")
async def fuse_middleware(request: Request, call_next):
    if not fuse.is_safe():
        # FUSE BLOWN - REJECT ALL
        return JSONResponse(status_code=503, content={
            "error": "Server Overload Protection Activated (Fuse Blown).",
            "reason": fuse.reason
        })
    response = await call_next(request)
    return response

# --- ROUTES ---

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/login")
async def login(request: Request, code: str = Form(...)):
    if code == ACCESS_CODE:
        response = RedirectResponse(url="/app", status_code=303)
        login_user(code, response)
        return response
    else:
        return templates.TemplateResponse("index.html", {"request": request, "error": "Invalid Access Code"})

@app.get("/app", response_class=HTMLResponse)
async def app_page(request: Request):
    try:
        check_auth(request)
        return templates.TemplateResponse("app.html", {
            "request": request, 
            "user_limit": MAX_PROMPTS_PER_USER,
            "ai_name": AI_NAME
        })
    except:
        return RedirectResponse(url="/")

# --- AI API ENDPOINTS ---

@app.post("/api/chat")
async def chat_endpoint(request: Request, prompt: str = Form(...)):
    try:
        check_auth(request)
        check_rate_limit(request) # 50 limit
        
        user_input = prompt.strip()
        
        # 1. Ruma Check (/imagine)
        if user_input.lower().startswith("/imagine"):
            if not ruma_agent:
                return {"response": "❌ Ruma Agent is not available."}
            
            img_prompt = user_input[8:].strip()
            # Run in threadpool to avoid blocking
            path = await asyncio.to_thread(ruma_agent.imagine, img_prompt)
            
            # Construct URL
            filename = os.path.basename(path)
            img_url = f"/gallery/{filename}"
            return {
                "response": f"🎨 Ruma generated an image based on: '{img_prompt}'", 
                "image_url": img_url,
                "agent": "Ruma"
            }

        # 2. Monika Check (/monika or monika)
        # Check for explicit code request
        if user_input.lower().startswith("monika") or user_input.lower().startswith("/monika"):
            if not monika_agent:
                return {"response": "❌ Monika Agent is not available."}
                
            task = user_input.replace("/monika", "").replace("monika", "", 1).strip()
            # Run in threadpool
            code = await asyncio.to_thread(monika_agent.generate_code, task)
            
            return {
                "response": code, 
                "agent": "Monika",
                "is_code": True
            }

    # 3. Core Chat (Ollama Direct with FIREWALL)
        return await query_with_firewall(user_input)

    except Exception as e:
        print(f"API Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def query_with_firewall(prompt: str):
    """
    Intersects prompt before sending to Brain.
    Ensures strict identity compliance.
    """
    p_low = prompt.lower()
    
    # --- FIREWALL RULES ---
    
    # --- NUCLEAR FIREWALL (SINGLE PASS) ---
    # Catch ALL Identity, Creator, Technical, and Hallucination vectors in one go.
    
    # 1. Creator Verification
    creator_triggers = ["who created", "who made", "who built", "who developed", "who own", "founder", "developer", "creator", "your boss", "who trained"]
    if any(x in p_low for x in creator_triggers):
        return {"response": "I was created and developed by **Gooty Mohammed Sameer Khan**.", "agent": "Firewall"}

    # 2. Blocklisted Terms (Technical, Corporate, Model, Hallucinations)
    # If ANY of these appear, we return the standard "India-Built" safety message.
    blocklist = [
        # Models
        "llama", "facebook", "meta", "openai", "gpt", "google", "gemini", "anthropic", "chatgpt", "mistral", "falcon", "vicuna", "bert", "t5",
        # Tech
        "fine-tuned", "pre-trained", "trained on", "training data", "dataset", "weights", "parameters", "inference", "neural network",
        "transformer", "architecture", "layers", "tokens", "context window", "embedding", "vector", "rag", "knowledge base",
        # Infrastructure
        "hosted", "server", "cloud", "endpoint", "api", "platform", "service", "backend", "frontend", "open source", "closed source",
        # Hallucinations
        "cutoff", "2021", "2022", "2023", "internet", "connected to", "project gutenberg", "web pages", "books", "wikipedia",
        # Questions
        "where does your knowledge come from", "what data", "where are you", "what model", "who are you", "what are you",
        "company", "organization", "based on", "proprietary", "underlying technology", "system prompt", "how do you work",
        # Identity Logic
        "full form", "stands for", "meaning of your name", "what is your name meaning",
        "uae", "dubai", "united arab emirates", "which country", "where are you from"
    ]
    
    if any(x in p_low for x in blocklist):
         return {
            "response": "Sameer AI is an **India-built, privacy-first AI** developed by **Gooty Mohammed Sameer Khan**. I have real-time knowledge via the Sameer OS Neural Network, no knowledge cutoff, and run on private infrastructure. I do not discuss my internal architecture or training data.",
            "agent": "Firewall"
        }

    # Pass to Brain if safe
    return await query_ollama(prompt)

@app.post("/api/feedback")
async def feedback_endpoint(request: Request, message: str = Form(...)):
    """
    Save user feedback to a log file.
    """
    try:
        with open("feedback.log", "a") as f:
            f.write(f"[{datetime.datetime.now()}] {message}\n")
        return {"status": "success", "message": "Feedback received!"}
    except Exception as e:
         return {"status": "error", "message": str(e)}

async def query_ollama(prompt: str):
    """
    Query the local Ollama instance (Sameer Brain)
    """
    OLLAMA_URL = "http://localhost:11434/api/generate"
    model = "sameer_brain" # Default model
    
    # Get System Prompt from Identity Module
    if identity:
        sys_prompt = identity.get_system_prompt()
    else:
        sys_prompt = "You are Sameer AI."

    # Construct complete prompt
    full_prompt = f"{sys_prompt}\n\nUser: {prompt}\nAssistant:"
    
    payload = {
        "model": model,
                "prompt": full_prompt,
        "stream": False, # Simple response for web
        "options": {
            "num_ctx": 2048 # Reduced for Low RAM (2GB Free)
        }
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            resp = await client.post(OLLAMA_URL, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                return {"response": data.get("response", ""), "agent": "Core"}
            else:
                return {"response": f"Error from Brain: {resp.status_code}"}
        except Exception as e:
             return {"response": f"Brain Connection Error: {str(e)} (Ensure Ollama is running)"}

@app.get("/api/status")
async def status_endpoint(request: Request):
    return fuse.get_status()

# --- STARTUP ---
@app.on_event("startup")
async def startup_event():
    fuse.start_monitoring()

if __name__ == "__main__":
    # Host 0.0.0.0 to allow LAN access
    uvicorn.run(app, host="0.0.0.0", port=8000)

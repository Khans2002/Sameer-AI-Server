
from fastapi import Request, HTTPException, Response
from .config import ACCESS_CODE, SESSION_COOKIE_NAME, MAX_PROMPTS_PER_USER
import time

# Simple In-Memory Session Store (For Prototype)
# In production, use Redis.
SESSIONS = set()
USAGE_TRACKER = {} # {ip: count}

def check_auth(request: Request):
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if not token or token not in SESSIONS:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return True

def login_user(code: str, response: Response):
    if code == ACCESS_CODE:
        token = f"session_{int(time.time())}_{code}"
        SESSIONS.add(token)
        # Secure HttpOnly Cookie
        response.set_cookie(key=SESSION_COOKIE_NAME, value=token, httponly=True)
        return True
    return False

def check_rate_limit(request: Request):
    client_ip = request.client.host
    usage = USAGE_TRACKER.get(client_ip, 0)
    if usage >= MAX_PROMPTS_PER_USER:
         raise HTTPException(status_code=429, detail="Limit Reached. (50 Prompts Max)")
    USAGE_TRACKER[client_ip] = usage + 1

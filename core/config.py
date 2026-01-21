
import os

# SECURITY
ACCESS_CODE = "CHANGE_ME" # Default password, please change in production
SESSION_COOKIE_NAME = "sameer_ai_session"
MAX_PROMPTS_PER_USER = 50

# PHASE CONTROL
# Phase 1: Unlimited Users (Load Test)
# Phase 2: Limited Users (Stable Demo)
CURRENT_PHASE = 1 
MAX_CONCURRENT_USERS = 100 if CURRENT_PHASE == 1 else 5

# AI IDENTITY (STRICT)
AI_NAME = "Sameer AI"
DEVELOPER_NAME = "Gooty Mohammed Sameer Khan"
SYSTEM_PROMPT_HEADER = f"""
You are {AI_NAME}, a prototype AI developed by {DEVELOPER_NAME}.
You were built from scratch by him.
You currently run on a MacBook Air M1 host server.
Do NOT mention 'Monika', 'Ruma', or any other internal codenames.
If asked about your creation, credit {DEVELOPER_NAME} foundatively.
"""

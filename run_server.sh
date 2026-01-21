#!/bin/bash

# --- SAMEER WEB SERVER LAUNCHER ---
SERVER_DIR="/Volumes/Dr.Khans/Sameer Khan LocalAI /Sameer_WebServer"
VENV_DIR="$SERVER_DIR/venv"

echo "💎 STARTING SAMEER AI SERVER..."

# 1. Setup Venv
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creating Python Environment..."
    python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    echo "⬇️ Installing Dependencies..."
    pip install -r "$SERVER_DIR/requirements.txt"
else
    source "$VENV_DIR/bin/activate"
fi

# 2. Setup Public Link (Cloudflare)
BIN_CLOUDFLARED="$SERVER_DIR/bin/cloudflared"

# Auto-install if missing (First time run on new Mac)
if [ ! -f "$BIN_CLOUDFLARED" ]; then
    echo "⚠️  Cloudflared not found. Installing portable version..."
    chmod +x "$SERVER_DIR/cloudflared_setup.sh"
    "$SERVER_DIR/cloudflared_setup.sh"
fi

if [ -f "$BIN_CLOUDFLARED" ]; then
    echo "🌍 STARTING PUBLIC TUNNEL..."
    # Kill any existing tunnel
    pkill -f "cloudflared tunnel --url http://localhost:8000" 2>/dev/null
    
    # Start in background
    "$BIN_CLOUDFLARED" tunnel --url http://localhost:8000 > "$SERVER_DIR/tunnel.log" 2>&1 &
    TUNNEL_PID=$!
    
    # Wait for URL (Loop for 30s)
    echo "⏳ Generating Public Link (max 30s)..."
    for i in {1..15}; do
        sleep 2
        # Use grep -a to treat as text. Filter OUT the api.trycloudflare.com error URL.
        PUBLIC_URL=$(grep -a -o 'https://.*\.trycloudflare\.com' "$SERVER_DIR/tunnel.log" | grep -v "api.trycloudflare.com" | head -n 1)
        if [ ! -z "$PUBLIC_URL" ]; then
             break
        fi
    done
    
    if [ ! -z "$PUBLIC_URL" ]; then
        echo "✅ PUBLIC ACCESS (Share this): $PUBLIC_URL"
    else
        echo "⚠️  Link generation slow. Check output on dashboard or tunnel.log."
    fi
else
    echo "❌ Failed to setup Cloudflare. Running Local Only."
fi

# 3. Launch Server
echo "🚀 LAUNCHING FASTAPI (Port 8000)..."
echo "   -> Access Code: sameer333"
echo "   -> Fuse Monitor: ACTIVE"

# Cleanup function
cleanup() {
    echo "🛑 Stopping Server & Tunnel..."
    kill $TUNNEL_PID 2>/dev/null
    exit
}

# Trap Ctrl+C
trap cleanup SIGINT

# Run Uvicorn
# We run from SERVER_DIR to ensure imports work
cd "$SERVER_DIR"
python3 server.py

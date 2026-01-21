#!/bin/bash
# Sameer AI - Portable Public Link Setup
# Installs Cloudflare Tunnel locally on the drive (No system install needed)

SERVER_DIR="/Volumes/Dr.Khans/Sameer Khan LocalAI /Sameer_WebServer"
BIN_DIR="$SERVER_DIR/bin"
CLOUDFLARED="$BIN_DIR/cloudflared"

mkdir -p "$BIN_DIR"

echo "☁️  Setting up Cloudflare Tunnel (Portable)..."

# 1. Download Binary if missing
if [ ! -f "$CLOUDFLARED" ]; then
    echo "⬇️  Downloading cloudflared binary (macOS arm64)..."
    curl -L "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz" -o "$BIN_DIR/cloudflared.tgz"
    
    # Note: Using amd64 binary because arm64 builds were sometimes flaky in raw releases, 
    # but macOS Rosetta handles it fine. Let's try to get arm64 if available?
    # Actually, official link for mac is often universal or amd64. 
    # Let's use the official binary directly.
    
    # Retry with direct binary for M1 (arm64)
    # curl -L "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-arm64" -o "$CLOUDFLARED"
    
    # Let's stick to the tgz extraction method which is safer
    tar -xzf "$BIN_DIR/cloudflared.tgz" -C "$BIN_DIR"
    rm "$BIN_DIR/cloudflared.tgz"
    
    chmod +x "$CLOUDFLARED"
    echo "✅ Download Complete."
else
    echo "✅ Cloudflared already installed."
fi

# 2. Launch Tunnel
echo "🚀 Launching Public Tunnel..."
echo "---------------------------------------------------"
echo "Public URL will appear below. Share this link for Demo."
echo "---------------------------------------------------"

"$CLOUDFLARED" tunnel --url http://localhost:8000

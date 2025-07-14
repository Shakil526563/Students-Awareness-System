#!/usr/bin/env python3
"""
Start backend server for Student Weather Awareness System
"""
import subprocess
import sys
import time
import os
from pathlib import Path

def start_backend():
    """Start Django backend server on port 8000"""
    print("🚀 Starting Backend Server (Django)...")
    try:
        backend_process = subprocess.Popen([
            sys.executable, "manage.py", "runserver", "127.0.0.1:8000"
        ], cwd=Path(__file__).parent)
        return backend_process
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def main():
    print("🌤️ Student Weather Awareness System")
    print("=" * 45)
    print("Starting backend server...")
    print("=" * 45)
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Failed to start backend server")
        return
    
    print("\n✅ Backend server started successfully!")
    print("=" * 45)
    print("🔗 Backend:  http://127.0.0.1:8000")
    print("=" * 45)
    print("⏹️  Press Ctrl+C to stop server")
    
    try:
        # Wait for process
        while True:
            if backend_process.poll() is not None:
                print("❌ Backend server stopped")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n⏹️ Stopping server...")
        backend_process.terminate()
        
        # Wait for process to stop
        backend_process.wait()
        
        print("✅ Server stopped")

if __name__ == "__main__":
    main()

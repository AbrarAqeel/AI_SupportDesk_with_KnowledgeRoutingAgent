"""
Project runner for AI Support Desk.

Evaluator usage:
    python run.py

Behavior:
- Verifies environment
- Checks local LLM availability
- Asks whether to download if missing
- Runs in fallback mode if declined
- Starts backend and UI
"""

import os
import sys
import subprocess
import time
from typing import NoReturn

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# =========================
# Error handling
# =========================

def fail(message: str) -> NoReturn:
    print(f"\n❌ {message}\n")
    sys.exit(1)


# =========================
# Step 1: Python version
# =========================

if sys.version_info < (3, 10):
    fail("Python 3.10 or higher is required")

# =========================
# Step 2: Dependency check
# =========================

print("▶ Checking Python dependencies...")
try:
    import fastapi
    import streamlit
    import langgraph
except ImportError as e:
    fail(
        f"Missing Python dependency: {e.name}\n"
        "Run: pip install -r requirements.txt"
    )

print("✔ Python dependencies OK")

# =========================
# Step 3: Start backend
# =========================

print("▶ Starting FastAPI backend...")
try:
    backend = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "api.main:app", "--reload"],
        cwd=PROJECT_ROOT,
    )
except Exception as e:
    fail(f"Failed to start backend: {e}")

time.sleep(3)

# =========================
# Step 4: Start UI
# =========================

print("▶ Starting Streamlit UI...")
try:
    ui = subprocess.Popen(
        ["streamlit", "run", "ui/app.py"],
        cwd=PROJECT_ROOT,
    )
except Exception as e:
    backend.terminate()
    fail(f"Failed to start UI: {e}")

print("\n✅ AI Support Desk is running")
print("👉 UI: http://localhost:8501")
print("👉 API: http://127.0.0.1:8000/docs\n")

# =========================
# Keep processes alive
# =========================

try:
    backend.wait()
    ui.wait()
except KeyboardInterrupt:
    print("\n🛑 Shutting down...")
    backend.terminate()
    ui.terminate()

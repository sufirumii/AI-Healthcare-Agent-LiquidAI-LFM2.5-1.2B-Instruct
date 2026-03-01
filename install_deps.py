"""
Installation helper for Medical AI Agent
Run this first to install all dependencies
"""

import subprocess
import sys
import os

def install_requirements():
"""Install all requirements"""
requirements = [
"torch",
"transformers",
"accelerate",
"sentence-transformers",
"gradio",
"fastapi",
"uvicorn",
"python-multipart",
"pandas",
"numpy",
"beautifulsoup4",
"lxml",
"requests",
"python-dotenv",
"pyyaml",
"pydantic",
"tqdm",
"colorama",
"rich"
]

print("📦 Installing requirements...")
for req in requirements:
print(f" Installing {req}...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", req])

print("✅ All requirements installed!")

if name == "main":
install_requirements()

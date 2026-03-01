#!/bin/bash

Medical AI Agent - Quick Start Script
echo "=========================================="
echo "🏥 Medical AI Agent - Quick Start"
echo "=========================================="

Check Python version
python_version=$(python3 --version 2>&1 | grep -Po '(?<=Python )\d+\.\d+')
if (( $(echo "$python_version < 3.8" | bc -l) )); then
echo "❌ Python 3.8+ required"
exit 1
fi
echo "✅ Python $python_version detected"

Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt -q

Check for .env file
if [ ! -f .env ]; then
echo "⚠️ No .env file found, creating from template"
cp .env.example .env
echo "✅ Please edit .env with your email"
fi

Create directories
mkdir -p data/cache logs

Run the agent
echo "🚀 Starting Medical AI Agent..."
echo "=========================================="
python app.py "$@"

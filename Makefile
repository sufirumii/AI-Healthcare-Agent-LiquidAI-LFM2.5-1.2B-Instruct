# Medical AI Agent Makefile

.PHONY: help install run docker-build docker-run clean

help:
@echo "Available commands:"
@echo " make install - Install dependencies"
@echo " make run - Run the agent"
@echo " make docker-build - Build Docker image"
@echo " make docker-run - Run Docker container"
@echo " make clean - Clean cache files"

install:
pip install -r requirements.txt

run:
python app.py

docker-build:
docker build -t medical-ai-agent .

docker-run:
docker run -p 7860:7860 medical-ai-agent

clean:
find . -type d -name "pycache" -exec rm -rf {} +
find . -type f -name ".pyc" -delete
rm -rf data/cache/
rm -rf logs/*.log

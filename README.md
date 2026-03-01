# Medical AI Agent

A medical AI assistant powered by the LiquidAI LFM2.5-1.2B-Instruct model for clinical conversations. It is designed to provide structured information, maintain context across interactions, and support future integration with medical knowledge bases.

## Features

- **Core Model**: Built on LiquidAI LFM2.5-1.2B-Instruct, a 1.2B parameter instruct-tuned model.
- **Contextual Memory**: Maintains conversation history to provide coherent, multi-turn interactions.
- **Structured Responses**: Delivers information in a clear, professional format with appropriate medical disclaimers.
- **Extensible Architecture**: Designed to incorporate external knowledge sources like MedlinePlus, WHO, and Mayo Clinic.
- **Analytics**: Tracks query counts and response times for performance monitoring.
- **Clean Interface**: A functional, no-frills user interface built with Gradio for clarity and ease of use.
- **Production-Oriented**: Includes configuration management, logging, and error handling.

## Project Structure
AI-Healthcare-Agent/
├── app.py # Main application entry point
├── config/
│ └── config.yaml # System configuration
├── src/
│ ├── medical_agent.py # Core agent logic
│ └── advanced_ui.py # User interface
├── data/ # Cache and storage
├── logs/ # Application logs
├── .env.example # Environment variable template
├── requirements.txt # Python dependencies
├── README.md # This document
├── run.sh # Quick start script
├── Dockerfile # Docker container definition
├── install_deps.py # Dependency installer
├── .gitignore
├── Makefile
├── setup.py # Package installer
└── CONTRIBUTING.md # Contribution guidelines

text

## Quick Start

Follow these steps to run the agent locally.

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/sufirumii/AI-Healthcare-Agent-LiquidAI-LFM2.5-1.2B-Instruct.git
    cd AI-Healthcare-Agent-LiquidAI-LFM2.5-1.2B-Instruct
Install dependencies

bash
pip install -r requirements.txt
Configure environment (Optional)

bash
cp .env.example .env
# Edit .env if you have API keys for external sources
Running the Agent
Start the application with:

bash
python app.py
Once running, open the provided Gradio URL (usually http://localhost:7860) in your browser to interact with the agent.

Advanced Usage
Command Line Options
You can specify the server port and host:

bash
python app.py --port 8080 --host 0.0.0.0
Using Docker
Build and run the agent in a Docker container:

bash
docker build -t medical-ai-agent .
docker run -p 7860:7860 medical-ai-agent
Performance
Model Size: 1.2 billion parameters

Average Response Time: 2-5 seconds

Context Memory: Maintains history for the duration of a session

Contributing
Contributions are welcome. Please review the CONTRIBUTING.md file for guidelines on how to propose changes, report issues, or submit improvements.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Disclaimer
This tool is for educational and informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of a qualified healthcare provider with any questions you may have regarding a medical condition.

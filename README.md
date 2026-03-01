# Medical AI Agent

**MedAgent** is a medical AI assistant powered by the LiquidAI LFM2.5-1.2B-Instruct model. It supports clinical-style conversations with conversation memory for context retention and delivers structured, evidence-informed responses. The system is designed for educational and research purposes, with planned integration of trusted medical knowledge sources.

## Features

- Core LLM: LiquidAI LFM2.5-1.2B-Instruct (1.2 billion parameters, instruction-tuned, 32K context length)
- Conversation Memory: Retains context across multiple turns in a session
- Structured Responses: Clear, professional formatting with medical disclaimers
- User Interface: Gradio-based interface for local interaction
- Extensibility: Architecture supports addition of external knowledge retrieval (e.g., MedlinePlus, WHO, Mayo Clinic)
- Monitoring: Basic logging and performance tracking (queries, response times)
- Deployment: Docker support and configurable via environment variables

## Project Structure
AI-Healthcare-Agent-LiquidAI-LFM2.5-1.2B-Instruct/
├── app.py                  # Main application entry point
├── config/                 # Configuration files
│   └── config.yaml
├── src/                    # Core source code
│   ├── medical_agent.py    # Agent logic and LLM integration
│   └── advanced_ui.py      # Gradio interface implementation
├── data/                   # Cache and persistent storage
│   └── cache/
├── logs/                   # Application logs
├── .env.example            # Environment variable template
├── requirements.txt        # Python dependencies
├── README.md               # This document
├── run.sh                  # Quick-start script
├── Dockerfile              # Docker container definition
├── install_deps.py         # Helper for dependency installation
├── Makefile                # Build and automation tasks
├── setup.py                # Package setup
└── CONTRIBUTING.md         # Contribution guidelines
text## Prerequisites

- Python 3.8 or higher
- Git
- (Optional) Docker for containerized deployment

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/sufirumii/AI-Healthcare-Agent-LiquidAI-LFM2.5-1.2B-Instruct.git
   cd AI-Healthcare-Agent-LiquidAI-LFM2.5-1.2B-Instruct

Install dependencies:Bashpip install -r requirements.txtAlternatively, use the helper script:Bashpython install_deps.py
(Optional) Configure environment variables:Bashcp .env.example .envEdit .env to include any required API keys for future knowledge sources.

Running the Application
Start the agent locally:
Bashpython app.py
The Gradio interface will be available at http://localhost:7860 (or the displayed URL).
Command-line Options
Customize the server:
Bashpython app.py --port 8080 --host 0.0.0.0
Docker Deployment
Build and run with Docker:
Bashdocker build -t medical-ai-agent .
docker run -p 7860:7860 medical-ai-agent
Performance Notes

Model Size: 1.2 billion parameters
Typical Response Time: 2–5 seconds (depending on hardware)
Context Handling: Session-based memory (resets on restart)

Knowledge Sources (Planned / Extensible)
Future versions will integrate:

MedlinePlus (U.S. National Library of Medicine)
World Health Organization (WHO)
Mayo Clinic
PubMed (research literature)

Current implementation focuses on model-driven responses with safe disclaimers.
Medical Disclaimer
This application is provided strictly for educational, research, and informational purposes. It is not a medical device, does not provide medical advice, diagnosis, or treatment recommendations, and must not be used as a substitute for professional healthcare services. Always consult a qualified healthcare provider for any medical concerns or decisions. The developers and contributors assume no liability for any use or misuse of this tool.
Contributing
Contributions are welcome. Please read CONTRIBUTING.md for details on how to report issues, propose changes, or submit pull requests.
License
This project is licensed under the MIT License. See the LICENSE file for the full text.

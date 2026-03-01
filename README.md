# Medical AI Agent

**MedAgent** is a medical AI assistant powered by the LiquidAI LFM2.5-1.2B-Instruct model.  
It supports clinical-style conversations with conversation memory for context retention and delivers structured, evidence-informed responses.  

The system is designed strictly for **educational and research purposes**, with planned integration of trusted medical knowledge sources.

## Features

- Core LLM: LiquidAI LFM2.5-1.2B-Instruct (1.2 billion parameters, instruction-tuned, 32K context length)
- Conversation Memory: Retains context across multiple turns within a session
- Structured Responses: Clear, professional formatting including mandatory medical disclaimers
- User Interface: Gradio-based web interface for local interaction
- Extensibility: Modular architecture supports future addition of external knowledge retrieval (e.g., MedlinePlus, WHO, Mayo Clinic)
- Monitoring: Basic logging and performance tracking (query count, response times)
- Deployment: Docker support and configuration via environment variables

## Project Structure

```text
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
Prerequisites

Python 3.8 or higher
Git
(Optional) Docker — for containerized deployment

Installation

Clone the repositoryBashgit clone https://github.com/sufirumii/AI-Healthcare-Agent-LiquidAI-LFM2.5-1.2B-Instruct.git
cd AI-Healthcare-Agent-LiquidAI-LFM2.5-1.2B-Instruct
Install dependenciesBashpip install -r requirements.txtAlternatively, use the provided helper script:Bashpython install_deps.py
(Optional) Configure environment variablesBashcp .env.example .envEdit .env and add any required API keys (for future knowledge sources).

Running the Application
Local run
Bashpython app.py
The Gradio interface will be available at http://localhost:7860 (or the URL shown in the terminal).
Command-line options
Customize host/port/share behavior:
Bashpython app.py --port 8080 --host 0.0.0.0 --share
Docker deployment
Bashdocker build -t medical-ai-agent .
docker run -p 7860:7860 medical-ai-agent
Performance Notes

Model size: 1.2 billion parameters
Typical response time: 2–5 seconds (hardware dependent)
Context handling: Session-based memory (resets on application restart)

Knowledge Sources (Planned / Extensible)
Future versions will integrate:

MedlinePlus (U.S. National Library of Medicine)
World Health Organization (WHO)
Mayo Clinic
PubMed (research literature)

Current version relies on model-generated responses with strict safety disclaimers.
Medical Disclaimer
This application is provided strictly for educational, research, and informational purposes only.
It is not a medical device, does not provide medical advice, diagnosis, or treatment recommendations, and must not be used as a substitute for professional healthcare services.
Always consult a qualified healthcare provider for any medical concerns or decisions.
The developers and contributors assume no liability for any use or misuse of this tool.
Contributing
Contributions are welcome.
Please read CONTRIBUTING.md for guidelines on reporting issues, proposing changes, or submitting pull requests.
License
This project is licensed under the MIT License.

"""
Medical AI Agent - Main Application
===================================
Production entry point with multiple interface options.
"""

import os
import argparse
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import local modules
from src.medical_agent import get_agent
from src.advanced_ui import create_advanced_ui

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Medical AI Agent")
    parser.add_argument("--config", type=str, default="config/config.yaml",
                       help="Path to config file")
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", 7860)),
                       help="Port to run the server on")
    parser.add_argument("--host", type=str, default=os.getenv("HOST", "0.0.0.0"),
                       help="Host to bind to")
    parser.add_argument("--share", action="store_true", default=True,
                       help="Create a public link")
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("🏥 Medical AI Agent - Starting...")
    logger.info("=" * 60)
    
    # Initialize agent
    agent = get_agent(args.config)
    agent.load_model()
    
    # Create UI
    demo = create_advanced_ui()
    
    # Launch
    logger.info(f"🚀 Launching on {args.host}:{args.port}")
    demo.launch(
        server_name=args.host,
        server_port=args.port,
        share=args.share,
        debug=False
    )

if __name__ == "__main__":
    main()

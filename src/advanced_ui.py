
"""
Medical AI Agent - Professional Clinical Interface
=================================================
Clean, powerful, no-nonsense medical interface.
"""

import gradio as gr
from datetime import datetime
from src.medical_agent import get_agent

# Clean, professional CSS
CUSTOM_CSS = """
:root {
  --primary: #0a4d8c;
  --primary-dark: #06315c;
  --bg-light: #f5f7fb;
  --bg-white: #ffffff;
  --border: #e2e8f0;
  --text-primary: #1a2639;
  --text-secondary: #4a5568;
  --shadow: 0 2px 8px rgba(0,0,0,0.05);
  --shadow-hover: 0 4px 16px rgba(0,0,0,0.1);
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: var(--bg-light);
  color: var(--text-primary);
}

.header {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  padding: 32px 40px;
  border-radius: 16px;
  margin-bottom: 24px;
  color: white;
}

.header h1 {
  font-size: 2.5rem;
  font-weight: 600;
  margin: 0 0 8px 0;
}

.header p {
  font-size: 1rem;
  opacity: 0.9;
  margin: 0;
}

.main-panel {
  background: var(--bg-white);
  border-radius: 16px;
  padding: 32px;
  box-shadow: var(--shadow);
  border: 1px solid var(--border);
}

.primary-button {
  background: var(--primary);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.primary-button:hover {
  background: var(--primary-dark);
}

.answer-box {
  background: var(--bg-white);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  margin: 16px 0;
  line-height: 1.6;
  white-space: pre-wrap;
  min-height: 200px;
  max-height: 500px;
  overflow-y: auto;
}

.source-card {
  background: var(--bg-light);
  border-left: 4px solid var(--primary);
  padding: 16px;
  border-radius: 8px;
  margin: 12px 0;
  font-size: 0.95rem;
}

.source-title {
  font-weight: 600;
  color: var(--primary);
  margin-bottom: 6px;
}

.source-link {
  color: var(--primary);
  text-decoration: none;
  font-size: 0.9rem;
}

.source-link:hover {
  text-decoration: underline;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-box {
  background: var(--bg-light);
  padding: 16px;
  border-radius: 12px;
  text-align: center;
}

.stat-number {
  font-size: 2rem;
  font-weight: 600;
  color: var(--primary);
  margin-bottom: 4px;
}

.stat-label {
  font-size: 0.85rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.disclaimer {
  background: #fef8e7;
  border: 1px solid #f9e5b7;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 0.9rem;
  color: #8a6e3a;
  margin: 16px 0;
}

.example-chip {
  display: inline-block;
  background: var(--bg-light);
  border: 1px solid var(--border);
  padding: 8px 16px;
  border-radius: 30px;
  font-size: 0.9rem;
  margin: 0 8px 8px 0;
  cursor: pointer;
  transition: all 0.2s;
}

.example-chip:hover {
  background: var(--primary);
  color: white;
  border-color: var(--primary);
}
"""

def create_advanced_ui():
    """Create the professional medical interface"""
    
    agent = get_agent()
    
    # Ensure model is loaded
    if not agent.initialized:
        agent.load_model()
    
    # Stats tracking
    stats = {
        'queries': 0,
        'sources_found': 0,
        'total_response_time': 0
    }
    
    def process_question(question, use_sources, history):
        """Process medical question and return answer"""
        print(f"Processing question: {question}")  # Debug print
        
        if not question or len(question.strip()) == 0:
            return "Please enter a valid question.", "", stats['queries'], stats['sources_found'], 0, history
        
        start = datetime.now()
        
        try:
            # Process query through agent
            result = agent.process_query(question, use_sources)
            answer = result['response']
            sources = result['sources']
            sources_used = result['sources_used']
            
            # Update stats
            elapsed = (datetime.now() - start).total_seconds()
            stats['queries'] += 1
            stats['total_response_time'] += elapsed
            stats['sources_found'] += len(sources)
            
            avg_time = round(stats['total_response_time'] / stats['queries'], 2)
            
            # Format sources
            sources_html = ""
            if sources:
                for r in sources[:3]:
                    sources_html += f"""
                    <div class="source-card">
                        <div class="source-title">{r.get('title', 'Unknown')[:150]}...</div>
                        <div style="color: #666; margin-bottom: 8px;">{r.get('source', 'Unknown')}</div>
                        <a href="{r.get('url', '#')}" target="_blank" class="source-link">View source →</a>
                    </div>
                    """
            else:
                sources_html = "<p style='color: #666;'>No external sources retrieved.</p>"
            
            # Update history
            if history is None:
                history = []
            history.append((question, answer[:200] + "..."))
            
            return answer, sources_html, stats['queries'], stats['sources_found'], avg_time, history
            
        except Exception as e:
            error_msg = f"Error processing question: {str(e)}"
            print(error_msg)
            return error_msg, "", stats['queries'], stats['sources_found'], 0, history
    
    # Function to handle example clicks
    def set_example(example, history):
        return example, history
    
    # Header
    header = """
    <div class="header">
        <h1>Medical Intelligence Platform</h1>
        <p>Clinical Decision Support System • Evidence-Based Medicine • Multi-Source Retrieval</p>
    </div>
    """
    
    with gr.Blocks(theme=gr.themes.Soft(), css=CUSTOM_CSS) as demo:
        gr.HTML(header)
        
        with gr.Row():
            with gr.Column(scale=2):
                # Main panel
                with gr.Group():
                    question = gr.Textbox(
                        label="Clinical Question",
                        placeholder="Enter your clinical question here...",
                        lines=3
                    )
                    
                    with gr.Row():
                        use_sources = gr.Checkbox(
                            label="Retrieve medical sources",
                            value=True
                        )
                        submit = gr.Button(
                            "Get Answer",
                            variant="primary"
                        )
                
                # Answer display
                answer = gr.Textbox(
                    label="Answer",
                    lines=10,
                    interactive=False
                )
                
                # Sources
                sources = gr.HTML(label="Sources")
                
                # Disclaimer
                disclaimer = """
                <div class="disclaimer">
                    This information is for educational purposes only. Always consult with a qualified healthcare provider.
                </div>
                """
                gr.HTML(disclaimer)
            
            with gr.Column(scale=1):
                # Stats
                with gr.Group():
                    gr.Markdown("### Analytics")
                    query_count = gr.Number(label="Total Queries", value=0)
                    source_count = gr.Number(label="Sources Found", value=0)
                    avg_time = gr.Number(label="Avg Response (s)", value=0)
                
                # Conversation history
                chatbot = gr.Chatbot(label="History", height=300)
                
                # Clear button
                clear = gr.Button("Clear Session", variant="secondary")
        
        # Examples
        gr.Markdown("### Clinical Queries")
        examples = [
            "What are the diagnostic criteria for diabetes mellitus?",
            "Explain the mechanism of action of insulin",
            "What are the current treatment guidelines for hypertension?",
            "Differential diagnosis of acute chest pain",
            "Evidence-based management of migraine headaches",
            "What are the first-line antibiotics for pneumonia?",
            "Diagnostic criteria for rheumatoid arthritis",
            "Treatment options for type 2 diabetes"
        ]
        
        # Create example buttons
        with gr.Row():
            for ex in examples[:4]:
                btn = gr.Button(ex[:30] + "...", size="sm")
                btn.click(fn=lambda x=ex: x, outputs=question)
        
        with gr.Row():
            for ex in examples[4:]:
                btn = gr.Button(ex[:30] + "...", size="sm")
                btn.click(fn=lambda x=ex: x, outputs=question)
        
        # Event handlers
        submit.click(
            fn=process_question,
            inputs=[question, use_sources, chatbot],
            outputs=[answer, sources, query_count, source_count, avg_time, chatbot]
        ).then(
            fn=lambda: None,
            inputs=None,
            outputs=None
        )
        
        clear.click(
            fn=lambda: ("", "", 0, 0, 0, []),
            inputs=None,
            outputs=[answer, sources, query_count, source_count, avg_time, chatbot]
        )
    
    return demo

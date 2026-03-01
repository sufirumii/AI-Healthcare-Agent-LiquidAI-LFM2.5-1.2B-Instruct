
"""
Medical AI Agent - Main Agent Class
===================================
Production-grade medical agent with tool use, memory, and multi-source retrieval.
"""

import os
import json
import yaml
import logging
import hashlib
import pickle
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field

import torch
import requests
from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class MedicalAgentConfig:
    """Configuration for Medical Agent"""
    model_name: str = "LiquidAI/LFM2.5-1.2B-Instruct"
    device: str = "auto"
    torch_dtype: str = "float16"
    use_quantization: bool = True
    max_length: int = 2048
    temperature: float = 0.3
    pubmed_email: str = ""
    pubmed_tool: str = "MedicalAI-Agent"
    max_pubmed_results: int = 5
    memory_size: int = 100
    cache_dir: str = "data/cache"


class MedicalKnowledgeBase:
    """Fetch medical information from various free APIs"""
    
    def __init__(self, config: MedicalAgentConfig):
        self.config = config
        self.cache = {}
        self.load_cache()
        
    def load_cache(self):
        """Load cached responses"""
        cache_file = Path(f"{self.config.cache_dir}/knowledge_cache.pkl")
        if cache_file.exists():
            with open(cache_file, 'rb') as f:
                self.cache = pickle.load(f)
            logger.info(f"Loaded {len(self.cache)} cached items")
    
    def save_cache(self):
        """Save cache to disk"""
        cache_file = Path(f"{self.config.cache_dir}/knowledge_cache.pkl")
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        with open(cache_file, 'wb') as f:
            pickle.dump(self.cache, f)
    
    def get_cache_key(self, query: str, source: str) -> str:
        """Generate cache key"""
        return hashlib.md5(f"{source}:{query}".encode()).hexdigest()
    
    def search_medline_plus(self, query: str) -> List[Dict]:
        """Search MedlinePlus for health information"""
        cache_key = self.get_cache_key(query, "medline")
        if cache_key in self.cache:
            return self.cache[cache_key]
            
        try:
            url = "https://wsearch.nlm.nih.gov/ws/query"
            params = {
                'db': 'healthTopics',
                'term': query,
                'retmax': 3
            }
            response = requests.get(url, params=params, timeout=5)
            results = []
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'xml')
                for doc in soup.find_all('document')[:3]:
                    title = doc.find('content', {'name': 'title'})
                    content = doc.find('content', {'name': 'fullSummary'})
                    if title and content:
                        results.append({
                            'title': title.text,
                            'content': content.text[:500],
                            'source': 'MedlinePlus',
                            'url': f"https://medlineplus.gov/{doc.get('url', '')}"
                        })
            
            self.cache[cache_key] = results
            self.save_cache()
            return results
        except Exception as e:
            logger.error(f"MedlinePlus search error: {e}")
            return []
    
    def search_who(self, query: str) -> List[Dict]:
        """Search WHO health topics"""
        cache_key = self.get_cache_key(query, "who")
        if cache_key in self.cache:
            return self.cache[cache_key]
            
        try:
            url = "https://www.who.int/api/search"
            params = {'q': query, 'type': 'topic'}
            response = requests.get(url, params=params, timeout=5)
            results = []
            
            if response.status_code == 200:
                data = response.json()
                for item in data.get('results', [])[:3]:
                    results.append({
                        'title': item.get('title', ''),
                        'content': item.get('description', '')[:500],
                        'source': 'World Health Organization',
                        'url': f"https://www.who.int{item.get('url', '')}"
                    })
            
            self.cache[cache_key] = results
            self.save_cache()
            return results
        except Exception as e:
            logger.error(f"WHO search error: {e}")
            return []
    
    def search_mayo_clinic(self, query: str) -> List[Dict]:
        """Search Mayo Clinic (scrapes with proper headers)"""
        cache_key = self.get_cache_key(query, "mayo")
        if cache_key in self.cache:
            return self.cache[cache_key]
            
        try:
            url = "https://www.mayoclinic.org/search/search-results"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            params = {'q': query}
            response = requests.get(url, params=params, headers=headers, timeout=5)
            results = []
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                for result in soup.find_all('div', class_='result')[:3]:
                    title = result.find('a')
                    desc = result.find('p')
                    if title and desc:
                        results.append({
                            'title': title.text.strip(),
                            'content': desc.text.strip()[:500],
                            'source': 'Mayo Clinic',
                            'url': f"https://www.mayoclinic.org{title.get('href', '')}"
                        })
            
            self.cache[cache_key] = results
            self.save_cache()
            return results
        except Exception as e:
            logger.error(f"Mayo Clinic search error: {e}")
            return []
    
    def get_combined_results(self, query: str) -> Tuple[List[Dict], str, str]:
        """Get results from all knowledge bases"""
        all_results = []
        sources_used = []
        
        # Search in parallel (simulated async)
        medline_results = self.search_medline_plus(query)
        if medline_results:
            all_results.extend(medline_results)
            sources_used.append("MedlinePlus")
            
        who_results = self.search_who(query)
        if who_results:
            all_results.extend(who_results)
            sources_used.append("WHO")
            
        mayo_results = self.search_mayo_clinic(query)
        if mayo_results:
            all_results.extend(mayo_results)
            sources_used.append("Mayo Clinic")
        
        # Format context
        context = ""
        for i, result in enumerate(all_results[:5], 1):
            context += f"\n[{i}] From {result['source']}: {result['title']}\n"
            context += f"{result['content']}\n"
            context += f"Source: {result['url']}\n"
        
        sources_text = ", ".join(set(sources_used)) if sources_used else "No external sources"
        
        return all_results, context, sources_text


class MedicalLLM:
    """Medical language model wrapper"""
    
    def __init__(self, config: MedicalAgentConfig):
        self.config = config
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        
    def load(self):
        """Load the model"""
        logger.info(f"Loading model: {self.config.model_name}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.config.model_name,
            trust_remote_code=True
        )
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Set torch dtype
        torch_dtype = torch.float16 if self.config.torch_dtype == "float16" else torch.float32
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.config.model_name,
            device_map=self.config.device,
            torch_dtype=torch_dtype,
            trust_remote_code=True,
            low_cpu_mem_usage=True
        )
        
        self.pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=self.config.max_length,
            temperature=self.config.temperature,
            do_sample=True
        )
        
        logger.info("Model loaded successfully")
    
    def generate(self, prompt: str, context: Optional[str] = None) -> str:
        """Generate response"""
        try:
            if context:
                full_prompt = f"{context}\n\nQuestion: {prompt}\n\nAnswer:"
            else:
                full_prompt = f"Question: {prompt}\n\nAnswer:"
            
            response = self.pipeline(full_prompt)[0]['generated_text']
            
            # Extract answer
            if "Answer:" in response:
                response = response.split("Answer:")[-1].strip()
            
            return response
        except Exception as e:
            logger.error(f"Generation error: {e}")
            return f"Error generating response: {str(e)}"


class MedicalAgent:
    """Production-ready Medical AI Agent"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        # Load config
        with open(config_path, 'r') as f:
            self.config_dict = yaml.safe_load(f)
        
        model_config = self.config_dict.get('model', {})
        self.config = MedicalAgentConfig(
            model_name=model_config.get('name', "LiquidAI/LFM2.5-1.2B-Instruct"),
            device=model_config.get('device', "auto"),
            torch_dtype=model_config.get('torch_dtype', "float16"),
            use_quantization=model_config.get('use_quantization', True),
            max_length=model_config.get('max_length', 2048),
            temperature=model_config.get('temperature', 0.3)
        )
        self.config.pubmed_email = os.getenv('PUBMED_EMAIL', 'your_email@example.com')
        
        # Initialize components
        self.knowledge_base = MedicalKnowledgeBase(self.config)
        self.llm = MedicalLLM(self.config)
        self.conversation_history = []
        self.initialized = False
        
        logger.info("Medical Agent initialized with config")
    
    def load_model(self):
        """Load the LLM model"""
        self.llm.load()
        self.initialized = True
    
    def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
        """Generate response using LLM"""
        return self.llm.generate(prompt, context)
    
    def process_query(self, query: str, use_external_sources: bool = True) -> Dict:
        """Process a medical query"""
        if not self.initialized:
            self.load_model()
        
        # Get external knowledge if enabled
        context = ""
        sources = []
        sources_used = ""
        
        if use_external_sources:
            results, context_text, sources_used = self.knowledge_base.get_combined_results(query)
            context = context_text
            sources = results
        
        # Generate response
        response = self.llm.generate(query, context if context else None)
        
        # Add to conversation history
        self.conversation_history.append({
            'query': query,
            'response': response,
            'sources': sources_used,
            'timestamp': datetime.now().isoformat()
        })
        
        # Trim history
        if len(self.conversation_history) > self.config.memory_size:
            self.conversation_history = self.conversation_history[-self.config.memory_size:]
        
        return {
            'query': query,
            'response': response,
            'sources': sources,
            'sources_used': sources_used,
            'conversation_id': len(self.conversation_history)
        }
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")


# Create singleton instance
_agent_instance = None

def get_agent(config_path: str = "config/config.yaml") -> MedicalAgent:
    """Get or create the agent singleton"""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = MedicalAgent(config_path)
    return _agent_instance

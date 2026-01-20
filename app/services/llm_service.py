"""
LLM Service

Handles all interactions with the Ollama LLM API.
"""
import requests
from pathlib import Path
from typing import Optional

from app.config.settings import settings


class LLMService:
    """Service for generating AI responses via Ollama."""
    
    def __init__(self):
        self.model = settings.GENERATIVE_AI_MODEL
        self.api_url = settings.GENERATIVE_AI_URL
    
    def load_prompt(
        self,
        prompt_path: Path,
        job_choice: str = "",
        max_questions: int = 0,
        resume_summary: str = "",
        chat_history: list = None
    ) -> str:
        """Load and populate a prompt template with dynamic values."""
        if not prompt_path.exists():
            print(f"Prompt file does not exist: {prompt_path}")
            return ""
        
        with prompt_path.open(encoding="utf-8") as f:
            prompt = f.read()
        
        # Replace placeholders
        prompt = prompt.replace("{job}", job_choice)
        prompt = prompt.replace("{nb_question}", str(max_questions))
        prompt = prompt.replace("{resume_summary}", resume_summary)
        
        if chat_history:
            history_text = "\n".join(
                f"{'User' if m['role'] == 'user' else 'Assistant'}: {m['content']}"
                for m in chat_history
            )
            prompt = prompt.replace("{chat_history}", history_text)
        else:
            prompt = prompt.replace("{chat_history}", "")
        
        return prompt
    
    def generate_response(
        self,
        prompt_path: Path,
        job_choice: str = "",
        max_questions: int = 0,
        resume_summary: str = "",
        chat_history: list = None,
        additional_text: str = ""
    ) -> str:
        """Generate a response from the LLM."""
        prompt = self.load_prompt(
            prompt_path,
            job_choice,
            max_questions,
            resume_summary,
            chat_history
        ) + additional_text
        
        print(prompt)  # Debug logging
        
        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            print(f"Erreur lors de la génération de la réponse : {e}")
            return "Erreur lors de la génération de la réponse."


# Singleton instance
llm_service = LLMService()

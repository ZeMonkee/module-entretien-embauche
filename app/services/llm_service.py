"""
LLM Service

Handles all interactions with the Ollama LLM API.
"""
import logging
from pathlib import Path
from typing import Optional

import requests

from app.config.settings import settings

logger = logging.getLogger(__name__)


class LLMService:
    """Service for generating AI responses via Ollama."""

    def __init__(self):
        self.model = settings.GENERATIVE_AI_MODEL
        self.api_url = settings.GENERATIVE_AI_URL
        self.timeout = settings.LLM_REQUEST_TIMEOUT

    def load_prompt(
        self,
        prompt_path: Path,
        job_choice: str = "",
        max_questions: int = 0,
        resume_summary: str = "",
        chat_history: Optional[list] = None,
    ) -> str:
        """Load and populate a prompt template with dynamic values.

        Args:
            prompt_path: Path to the prompt template file
            job_choice: Target job position
            max_questions: Maximum number of interview questions
            resume_summary: Summary of the candidate's resume
            chat_history: List of chat message dicts with 'role' and 'content'

        Returns:
            Populated prompt string, or empty string if file not found
        """
        if not prompt_path.exists():
            logger.error("Prompt file does not exist: %s", prompt_path)
            return ""

        with prompt_path.open(encoding="utf-8") as f:
            prompt = f.read()

        prompt = prompt.replace("{job}", job_choice)
        prompt = prompt.replace("{nb_question}", str(max_questions))
        prompt = prompt.replace("{resume_summary}", resume_summary)

        if chat_history:
            history_text = "\n".join(
                f"{'Candidat' if m['role'] == 'user' else 'Recruteur'}: {m['content']}"
                for m in chat_history
            )
            prompt = prompt.replace("{chat_history}", history_text)
        else:
            prompt = prompt.replace("{chat_history}", "Aucun échange pour le moment.")

        return prompt

    def generate_response(
        self,
        prompt_path: Path,
        job_choice: str = "",
        max_questions: int = 0,
        resume_summary: str = "",
        chat_history: Optional[list] = None,
        additional_text: str = "",
    ) -> str:
        """Generate a response from the LLM.

        Args:
            prompt_path: Path to the prompt template file
            job_choice: Target job position
            max_questions: Maximum number of interview questions
            resume_summary: Summary of the candidate's resume
            chat_history: List of chat message dicts
            additional_text: Extra text appended to the prompt

        Returns:
            Generated response text, or error message on failure
        """
        prompt = self.load_prompt(
            prompt_path, job_choice, max_questions, resume_summary, chat_history
        )

        if additional_text:
            prompt = f"{prompt}\n\n{additional_text}"

        logger.debug("Sending prompt to LLM:\n%s", prompt)

        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()["response"]
        except requests.Timeout:
            logger.error("LLM request timed out after %ds", self.timeout)
            return (
                "Le serveur IA met trop de temps à répondre. "
                "Veuillez réessayer."
            )
        except requests.ConnectionError:
            logger.error("Cannot connect to Ollama at %s", self.api_url)
            return (
                "Impossible de se connecter au serveur Ollama. "
                "Vérifiez qu'il est lancé."
            )
        except requests.HTTPError as e:
            logger.error("LLM HTTP error: %s", e)
            return "Erreur du serveur IA. Veuillez réessayer."
        except (KeyError, ValueError) as e:
            logger.error("Unexpected LLM response format: %s", e)
            return "Réponse inattendue du serveur IA."


llm_service = LLMService()

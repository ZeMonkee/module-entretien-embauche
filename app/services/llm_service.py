"""
LLM Service

Handles all interactions with the Ollama LLM API.
"""
import requests
import logging
from pathlib import Path
from typing import Optional
import os

from app.config.settings import settings

# Configure logging
logging.basicConfig()
logger = logging.getLogger("llm_service")
logger.setLevel(logging.INFO)


class LLMService:
    """Service for generating AI responses via Ollama."""

    def __init__(self):
        self.model = settings.GENERATIVE_AI_MODEL
        self.api_url = settings.GENERATIVE_AI_URL
        self._ssh_tunnel = None

        if settings.SSH_ENABLED:
            self._start_ssh_tunnel()

    def _start_ssh_tunnel(self):
        """Start the SSH tunnel if configured."""
        try:
            # Fix for paramiko > 3.0 incompatibility with sshtunnel
            import paramiko
            if not hasattr(paramiko, "DSSKey"):
                 logger.warning("Patching paramiko.DSSKey for sshtunnel compatibility")
                 class DSSKey:
                     pass
                 paramiko.DSSKey = DSSKey

            from sshtunnel import SSHTunnelForwarder

            # Pre-flight: Ensure host is known
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                mypath = os.path.expanduser('~/.ssh/known_hosts')
                if os.path.exists(mypath):
                    client.load_host_keys(mypath)

                pkey = None
                if settings.SSH_KEY_PATH and os.path.exists(settings.SSH_KEY_PATH):
                     pkey = paramiko.RSAKey.from_private_key_file(settings.SSH_KEY_PATH)

                try:
                    client.connect(
                        settings.SSH_HOST,
                        port=22,
                        username=settings.SSH_USERNAME,
                        password=settings.SSH_PASSWORD,
                        pkey=pkey,
                        allow_agent=True,
                        look_for_keys=False,
                        timeout=5
                    )
                    if not os.path.exists(os.path.dirname(mypath)):
                         os.makedirs(os.path.dirname(mypath), exist_ok=True)
                    client.save_host_keys(mypath)
                    client.close()
                except Exception as e:
                    logger.warning(f"Pre-flight connection warning: {e}")
            except Exception as e:
                logger.error(f"Failed to auto-add host key: {e}")

            ssh_args = {
                "ssh_address_or_host": (settings.SSH_HOST, 22),
                "ssh_username": settings.SSH_USERNAME,
                "remote_bind_address": ("localhost", settings.SSH_LLM_REMOTE_BIND_PORT),
                "local_bind_address": ("localhost", settings.SSH_LLM_LOCAL_BIND_PORT),
                "allow_agent": True,
            }

            if settings.SSH_PASSWORD:
                ssh_args["ssh_password"] = settings.SSH_PASSWORD

            if settings.SSH_KEY_PATH:
                ssh_args["ssh_pkey"] = settings.SSH_KEY_PATH

            self._ssh_tunnel = SSHTunnelForwarder(**ssh_args)
            self._ssh_tunnel.start()
            logger.info(f"LLM SSH Tunnel established: localhost:{settings.SSH_LLM_LOCAL_BIND_PORT} -> {settings.SSH_HOST}:localhost:{settings.SSH_LLM_REMOTE_BIND_PORT}")

        except Exception as e:
            logger.error(f"Failed to start LLM SSH tunnel: {e}")

    def __del__(self):
        if self._ssh_tunnel:
            self._ssh_tunnel.stop()

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

"""
Application Settings and Configuration

Centralizes all configuration parameters for the interview module.
Uses environment variables with sensible defaults.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROMPTS_DIR = BASE_DIR / "prompts"


class Settings:
    """Application configuration settings."""

    # Configuration Ollama
    # Pour serveur distant via tunnel SSH : 'ssh -L 11434:localhost:11434 p2300557@iutbg-skynet.iutbourg.univ-lyon1.fr'
    # Puis utilisez "http://localhost:11434" pour accéder au serveur distant
    GENERATIVE_AI_MODEL: str = "llama3.3:latest"  # Modèle Llama 3.3
    GENERATIVE_AI_URL: str = "http://localhost:11434/api/generate"

    # Prompt file paths
    INTERVIEW_PROMPT_PATH: Path = PROMPTS_DIR / "interview_prompt.txt"
    RESULTS_PROMPT_PATH: Path = PROMPTS_DIR / "results_prompt.txt"
    SUMMARIZE_RESUME_PROMPT_PATH: Path = PROMPTS_DIR / "summarize_resume_prompt.txt"

    # Interview defaults
    DEFAULT_MAX_QUESTIONS: int = 3
    DEFAULT_JOB_CHOICE: str = "non défini"

    # Audio configuration
    WHISPER_MODEL: str = os.getenv("WHISPER_MODEL", "tiny")
    WHISPER_COMPUTE_TYPE: str = "int8_float32"
    WHISPER_DEVICE: str = "cpu"
    WHISPER_CPU_THREADS: int = int(os.getenv("WHISPER_THREADS", "8"))
    AUDIO_LANGUAGE: str = "fr"

    # TTS Configuration (EDGE-TTS)
    TTS_ENABLED: bool = True
    # Voix Microsoft Edge (Ex: 'fr-FR-HenriNeural', 'fr-FR-DeniseNeural')
    TTS_VOICE_ID: str = "fr-FR-HenriNeural"

    # SSH Tunneling (LLM Only now)
    SSH_ENABLED: bool = True
    SSH_HOST: str = os.getenv("SSH_HOST", "iutbg-skynet.iutbourg.univ-lyon1.fr")
    SSH_USERNAME: str = os.getenv("SSH_USERNAME", "p2300557")
    SSH_PASSWORD: str = os.getenv("SSH_PASSWORD", "")
    SSH_KEY_PATH: str = os.getenv("SSH_KEY_PATH", "")

    # -- LLM Configuration (Conserved for Ollama interaction if needed) --
    SSH_LLM_REMOTE_BIND_PORT: int = 11434
    SSH_LLM_LOCAL_BIND_PORT: int = 11434



settings = Settings()

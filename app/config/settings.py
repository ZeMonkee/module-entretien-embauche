"""
Application Settings and Configuration

Centralizes all configuration parameters for the interview module.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base paths
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
    WHISPER_MODEL: str = "tiny"
    WHISPER_COMPUTE_TYPE: str = "int8_float32"
    WHISPER_DEVICE: str = "cpu"
    WHISPER_CPU_THREADS: int = 8
    AUDIO_LANGUAGE: str = "fr"
    MAX_AUDIO_LENGTH: int = 60

    # TTS Configuration (Edge-TTS Natural + Local Fallback)
    TTS_ENABLED: bool = True
    # Voix recommandée: 'fr-FR-HenriNeural' ou 'fr-FR-DeniseNeural' pour une voix naturelle (nécessite Internet)
    # Si Internet indisponible, pyttsx3 (robotic) sera utilisé.
    TTS_VOICE_ID: str = "fr-FR-HenriNeural"

    # SSH Tunneling (LLM Only)
    SSH_ENABLED: bool = True
    SSH_HOST: str = os.getenv("SSH_HOST", "iutbg-skynet.iutbourg.univ-lyon1.fr")
    SSH_USERNAME: str = os.getenv("SSH_USERNAME", "p2300557")
    SSH_PASSWORD: str = os.getenv("SSH_PASSWORD", "")
    SSH_KEY_PATH: str = os.getenv("SSH_KEY_PATH", "")

    # -- LLM Configuration (Conserved for Ollama interaction) --
    SSH_LLM_REMOTE_BIND_PORT: int = 11434
    SSH_LLM_LOCAL_BIND_PORT: int = 11434



# Global settings instance
settings = Settings()

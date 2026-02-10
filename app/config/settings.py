"""
Application Settings and Configuration

Centralizes all configuration parameters for the interview module.
Uses environment variables with sensible defaults.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROMPTS_DIR = BASE_DIR / "prompts"


class Settings:
    """Application configuration settings."""

    # LLM Configuration
    GENERATIVE_AI_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    GENERATIVE_AI_URL: str = os.getenv(
        "OLLAMA_URL", "http://localhost:11434/api/generate"
    )
    LLM_REQUEST_TIMEOUT: int = int(os.getenv("LLM_TIMEOUT", "120"))

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


settings = Settings()

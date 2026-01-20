"""
Application Settings and Configuration

Centralizes all configuration parameters for the interview module.
"""
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROMPTS_DIR = BASE_DIR / "prompts"


class Settings:
    """Application configuration settings."""
    
    # LLM Configuration
    GENERATIVE_AI_MODEL: str = "llama3.1:8b"
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


# Global settings instance
settings = Settings()

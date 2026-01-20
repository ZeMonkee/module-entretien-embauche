"""
Audio Service

Handles audio transcription using Whisper.
"""
from datetime import datetime
import os
import shutil
import logging
from typing import Optional

from app.config.settings import settings

# Configure logging
logging.basicConfig()
logging.getLogger("faster_whisper").setLevel(logging.DEBUG)


class AudioService:
    """Service for audio transcription using Whisper (lazy loading)."""
    
    def __init__(self):
        self._model: Optional["WhisperModel"] = None
        self.language = settings.AUDIO_LANGUAGE
    
    @property
    def model(self):
        """Lazy load the Whisper model on first use."""
        if self._model is None:
            from faster_whisper import WhisperModel
            self._model = WhisperModel(
                settings.WHISPER_MODEL,
                compute_type=settings.WHISPER_COMPUTE_TYPE,
                device=settings.WHISPER_DEVICE,
                cpu_threads=settings.WHISPER_CPU_THREADS
            )
        return self._model
    
    def transcribe(self, audio_filepath: str) -> str:
        """
        Transcribe an audio file to text.
        
        Args:
            audio_filepath: Path to the audio file
            
        Returns:
            Transcribed text
        """
        # Safe copy to avoid permission issues
        filename = f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        local_path = os.path.join(os.getcwd(), filename)
        shutil.copyfile(audio_filepath, local_path)
        
        try:
            segments, _ = self.model.transcribe(local_path, language=self.language)
            segments = list(segments)
            return " ".join([seg.text for seg in segments])
        finally:
            # Clean up temp file
            if os.path.exists(local_path):
                os.remove(local_path)


# Singleton instance
audio_service = AudioService()


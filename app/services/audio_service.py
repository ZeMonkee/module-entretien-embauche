"""
Audio Service

Handles audio transcription using Whisper.
"""
import logging
import os
import shutil
import tempfile
from datetime import datetime
from typing import Optional

from app.config.settings import settings

logger = logging.getLogger(__name__)


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

            logger.info(
                "Loading Whisper model '%s' (device=%s, compute=%s)",
                settings.WHISPER_MODEL,
                settings.WHISPER_DEVICE,
                settings.WHISPER_COMPUTE_TYPE,
            )
            self._model = WhisperModel(
                settings.WHISPER_MODEL,
                compute_type=settings.WHISPER_COMPUTE_TYPE,
                device=settings.WHISPER_DEVICE,
                cpu_threads=settings.WHISPER_CPU_THREADS,
            )
        return self._model

    def transcribe(self, audio_filepath: str) -> str:
        """Transcribe an audio file to text.

        Creates a safe temporary copy to avoid file permission issues,
        then transcribes it and cleans up.

        Args:
            audio_filepath: Path to the audio file

        Returns:
            Transcribed text, or empty string on failure
        """
        if not audio_filepath or not os.path.exists(audio_filepath):
            logger.warning("Audio file not found: %s", audio_filepath)
            return ""

        local_path = None
        try:
            suffix = os.path.splitext(audio_filepath)[1] or ".wav"
            fd, local_path = tempfile.mkstemp(suffix=suffix, prefix="interview_audio_")
            os.close(fd)
            shutil.copyfile(audio_filepath, local_path)

            segments, info = self.model.transcribe(
                local_path, language=self.language
            )
            text = " ".join(seg.text for seg in segments).strip()
            logger.info("Transcription completed: %d characters", len(text))
            return text

        except Exception:
            logger.exception("Audio transcription failed for: %s", audio_filepath)
            return ""

        finally:
            if local_path and os.path.exists(local_path):
                os.remove(local_path)


audio_service = AudioService()

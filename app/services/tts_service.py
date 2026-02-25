"""
TTS Service (Local pyttsx3 + Edge-TTS)

Hands text-to-speech generation.
Ideally uses Microsoft Edge TTS (Natural, Online) for quality.
Falls back to pyttsx3 (SAPI5, Offline, Robotic) if offline or error.
"""
import os
import logging
import asyncio
import edge_tts
import pyttsx3
from typing import Optional
from datetime import datetime

from app.config.settings import settings

# Configure logging
logging.basicConfig()
logger = logging.getLogger("tts_service")
logger.setLevel(logging.INFO)


class TTSService:
    """Service for Text-to-Speech generation using Edge-TTS (Natural) with pyttsx3 fallback."""

    def __init__(self):
        # Initialize fallback engine just in case
        try:
            self.fallback_engine = pyttsx3.init()
            self.fallback_engine.setProperty('rate', 175)
        except:
            self.fallback_engine = None

    async def _generate_edge_tts(self, text: str, voice: str, filepath: str) -> bool:
        """Generate audio using Edge-TTS (Returns True if successful)."""
        try:
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(filepath)
            return True
        except Exception as e:
            logger.warning(f"Edge-TTS failed (network issue?): {e}")
            return False

    def _generate_pyttsx3(self, text: str, filepath: str):
        """Generate audio using local SAPI5 (Robotic fallback)."""
        if not self.fallback_engine:
            return None
        try:
            self.fallback_engine.save_to_file(text, filepath)
            self.fallback_engine.runAndWait()
            return filepath
        except Exception as e:
            logger.error(f"pyttsx3 fallback failed: {e}")
            return None

    def generate_audio(self, text: str) -> Optional[str]:
        """
        Generate audio from text.
        Tries Edge-TTS first (Natural), then falls back to pyttsx3 (Robotic).
        """
        if not settings.TTS_ENABLED:
            return None

        if not text or not text.strip():
            return None

        # Create audio directory if not exists
        output_dir = os.path.join(os.getcwd(), "app", "static", "audio")
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')

        # Try Edge-TTS High Quality Voice first
        filename_edge = f"tts_{timestamp}.mp3"
        filepath_edge = os.path.join(output_dir, filename_edge)

        try:
            success = asyncio.run(self._generate_edge_tts(text, settings.TTS_VOICE_ID, filepath_edge))
            if success:
                logger.info(f"Audio generated (Edge-TTS Natural): {filepath_edge}")
                return filepath_edge
        except Exception as e:
            logger.error(f"Edge-TTS critical error: {e}")

        # Fallback to Robotic Voice
        logger.info("Falling back to local SAPI5 voice...")
        filename_robot = f"tts_{timestamp}.wav"
        filepath_robot = os.path.join(output_dir, filename_robot)
        return self._generate_pyttsx3(text, filepath_robot)


# Singleton instance
tts_service = TTSService()

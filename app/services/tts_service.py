"""
TTS Service (Local Edge-TTS)

Handles text-to-speech generation using Microsoft Edge TTS (free, high quality).
No remote server needed for voice.
"""
import os
import logging
import asyncio
import edge_tts
from typing import Optional
from datetime import datetime

from app.config.settings import settings

# Configure logging
logging.basicConfig()
logger = logging.getLogger("tts_service")
logger.setLevel(logging.INFO)


class TTSService:
    """Service for Text-to-Speech generation using Edge-TTS."""

    def __init__(self):
        self.voice_id = settings.TTS_VOICE_ID
        # No SSH tunnel needed for TTS anymore

    def generate_audio(self, text: str) -> Optional[str]:
        """
        Generate audio from text using Edge TTS (async wrapper).
        """
        if not settings.TTS_ENABLED:
            return None

        if not text or not text.strip():
            return None

        # Edge-TTS is async, so we need to run it in an event loop
        try:
            return asyncio.run(self._generate_audio_async(text))
        except Exception as e:
            logger.error(f"TTS Generation failed: {e}")
            return None

    async def _generate_audio_async(self, text: str) -> Optional[str]:
        """Async implementation of audio generation."""
        try:
            communicate = edge_tts.Communicate(text, self.voice_id)

            # Create audio directory if not exists
            output_dir = os.path.join(os.getcwd(), "app", "static", "audio")
            os.makedirs(output_dir, exist_ok=True)

            filename = f"tts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
            filepath = os.path.join(output_dir, filename)

            await communicate.save(filepath)

            logger.info(f"Audio generated: {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"Edge-TTS async error: {e}")
            return None


# Singleton instance
tts_service = TTSService()

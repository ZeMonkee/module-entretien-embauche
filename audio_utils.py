from datetime import datetime
from faster_whisper import WhisperModel
import os
import shutil
import logging

logging.basicConfig()
logging.getLogger("faster_whisper").setLevel(logging.DEBUG)

model = WhisperModel(
    "tiny",
    compute_type="int8_float32",
    device="cpu",
    cpu_threads=8
)

def transcribe_audio(audio_filepath):
    """Transcribe an audio file with the model"""
    # Safe copy to avoid permission issues
    filename = f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    local_path = os.path.join(os.getcwd(), filename)
    shutil.copyfile(audio_filepath, local_path)

    try:
        # Use the copied file for transcription
        segments, _ = model.transcribe(local_path, language="fr")
        segments = list(segments)
        return " ".join([seg.text for seg in segments])
    finally:
        # Remove the temp audio file
        if os.path.exists(local_path):
            os.remove(local_path)

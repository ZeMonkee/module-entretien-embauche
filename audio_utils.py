import asyncio
import edge_tts
import os
import time
from faster_whisper import WhisperModel
from datetime import datetime
import shutil

# --- CONFIGURATION ---
VOICE = "fr-FR-RemyMultilingualNeural"

async def generate_voice(text, output_file):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_file)

def speak(text):
    unique_filename = f"tts_{int(time.time())}.mp3"

    try:
        asyncio.run(generate_voice(text, unique_filename))

        if os.path.exists(unique_filename):
            return unique_filename
        else:
            return None
    except Exception as e:
        print(f"Erreur TTS: {e}")
        return None

# --- WHISPER (Inchangé) ---
model = WhisperModel("medium", compute_type="int8", device="cpu")

def transcribe_audio(audio_filepath):
    if audio_filepath is None: return ""
    filename = f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    local_path = os.path.join(os.getcwd(), filename)
    shutil.copyfile(audio_filepath, local_path)
    try:
        segments, _ = model.transcribe(local_path, language="fr")
        text = " ".join([seg.text for seg in segments])
    finally:
        if os.path.exists(local_path):
            os.remove(local_path)
    return text

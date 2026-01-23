import asyncio
import edge_tts
import pygame
import os
import time
from faster_whisper import WhisperModel
from datetime import datetime
import shutil

# --- CONFIGURATION ---
# Voix : "fr-FR-HenriNeural" (Homme) ou "fr-FR-VivienneNeural" (Femme)
# "fr-FR-RemyMultilingualNeural" est aussi top.
VOICE = "fr-FR-HenriNeural"

async def generate_voice(text, output_file):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_file)

def speak(text):
    # Nom unique pour éviter le cache
    unique_filename = f"tts_{int(time.time())}.mp3"

    print(f"🗣️ Vocalisation (Microsoft) : '{text[:30]}...'")

    try:
        asyncio.run(generate_voice(text, unique_filename))

        if not os.path.exists(unique_filename):
            print("❌ ERREUR : Fichier audio non créé.")
            return

        pygame.mixer.init()
        pygame.mixer.music.load(unique_filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.quit()

    except Exception as e:
        print(f"❌ Erreur TTS : {e}")

    finally:
        if os.path.exists(unique_filename):
            try:
                os.remove(unique_filename)
            except:
                pass

# --- WHISPER (Reconnaissance) ---
model = WhisperModel("medium", compute_type="int8", device="cpu")

def transcribe_audio(audio_filepath):
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

from datetime import datetime
from faster_whisper import WhisperModel
import os
import shutil
import logging

logging.basicConfig()
logging.getLogger("faster_whisper").setLevel(logging.DEBUG)

model = WhisperModel("medium", compute_type="int8", device="cpu")

'''
Transcribe an audio file with the model above
@audio_filepath : the path of the audio file
'''
def transcribe_audio(audio_filepath):
    # Safe copy to avoid permission deny
    filename = f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    local_path = os.path.join(os.getcwd(), filename)  # saves to the project folder
    shutil.copyfile(audio_filepath, local_path)

    try:
        # Transcript the audio
        segments, _ = model.transcribe(audio_filepath, language="fr")
        segments = list(segments)
    finally:
        # Remove the temp audio file
        if os.path.exists(local_path):
            os.remove(local_path)

    return " ".join([seg.text for seg in segments])
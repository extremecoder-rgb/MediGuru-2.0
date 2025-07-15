
from dotenv import load_dotenv
load_dotenv()

import logging
import os
import tempfile
from pydub import AudioSegment
from scipy.io.wavfile import write
import sounddevice as sd
import numpy as np
from io import BytesIO


from groq import Groq

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def record_audio(file_path, duration=7, sample_rate=44100):
    """
    Records audio using sounddevice and saves it as an MP3.

    Args:
        file_path (str): Path to save the recorded audio file.
        duration (int): Duration of the recording in seconds.
        sample_rate (int): Sampling rate for audio.
    """
    try:
        logging.info("Recording audio... Speak now.")
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        sd.wait()

       
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
            write(temp_wav.name, sample_rate, audio)
            temp_wav_path = temp_wav.name

        
        sound = AudioSegment.from_wav(temp_wav_path)
        sound.export(file_path, format="mp3", bitrate="128k")
        os.remove(temp_wav_path)

        logging.info(f"Audio saved to {file_path}")
    except Exception as e:
        logging.error(f"An error occurred while recording: {e}")


def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):
    """
    Transcribes MP3 audio using Groq's Whisper model.

    Args:
        stt_model (str): Whisper model name.
        audio_filepath (str): Path to MP3 file.
        GROQ_API_KEY (str): API key from Groq.

    Returns:
        str: Transcribed text.
    """
    client = Groq(api_key=GROQ_API_KEY)

    with open(audio_filepath, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model=stt_model,
            file=audio_file,
            language="en"
        )

    return transcription.text



if __name__ == "__main__":
    
    audio_filepath = "patient_voice_test_for_patient.mp3"

 
    record_audio(file_path=audio_filepath, duration=7)

    
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    stt_model = "whisper-large-v3"

    if GROQ_API_KEY:
        text = transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY)
        print("\n📝 Transcription:\n", text)
    else:
        logging.error("GROQ_API_KEY not found in environment variables.")

from dotenv import load_dotenv
load_dotenv()

import os
from gtts import gTTS
from playsound import playsound  


def text_to_speech_with_gtts(input_text, output_filepath):
    """
    Converts input text to speech using Google Text-to-Speech and saves it as an MP3.
    Automatically plays the audio file after saving.

    Args:
        input_text (str): Text to be converted to speech.
        output_filepath (str): Path where the MP3 will be saved.
    """
    language = "en"

    try:
        # Generate and save audio
        tts = gTTS(text=input_text, lang=language, slow=False)
        tts.save(output_filepath)
        print(f"✅ Audio saved to {output_filepath}")

        # Play the audio file
        playsound(output_filepath)

    except Exception as e:
        print(f"❌ Error: {e}")


# === Example Usage ===
if __name__ == "__main__":
    input_text = "Hi, this is AI with Subhranil, using Google Text-to-Speech with autoplay!"
    output_mp3 = "gtts_output_autoplay.mp3"
    text_to_speech_with_gtts(input_text, output_mp3)

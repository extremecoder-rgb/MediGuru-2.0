from dotenv import load_dotenv
load_dotenv()

import os
import gradio as gr
from typing import Tuple

from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import record_audio, transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_gtts

system_prompt = """
You have to act as a professional doctor, I know you are not but this is for learning purpose.
What's in this image? Do you find anything wrong with it medically?
If you make a differential, suggest some remedies for them. Do not add any numbers or special characters in 
your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
Do not say 'In the image I see' but say 'With what I see, I think you have ....'
Don’t respond as an AI model in markdown, your answer should mimic that of an actual doctor, not an AI bot. 
Keep your answer concise (max 2 sentences). No preamble, start your answer right away please.
"""


def process_inputs(audio_filepath: str, image_filepath: str) -> Tuple[str, str, str]:
    if not audio_filepath:
        return "No audio provided", "Cannot generate doctor's response without audio.", None

    # Step 1: Transcribe audio
    speech_to_text_output = transcribe_with_groq(
        GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
        audio_filepath=audio_filepath,
        stt_model="whisper-large-v3"
    )

    # Step 2: Analyze image with context
    if image_filepath:
        doctor_response = analyze_image_with_query(
            query=system_prompt + speech_to_text_output,
            encoded_image=encode_image(image_filepath),
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
    else:
        doctor_response = "No image provided for me to analyze."

    # Step 3: Convert doctor's response to speech using gTTS
    audio_output_path = "final_response.mp3"
    text_to_speech_with_gtts(input_text=doctor_response, output_filepath=audio_output_path)

    return speech_to_text_output, doctor_response, audio_output_path



# Build Gradio interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath", label="Speak your symptoms"),
        gr.Image(type="filepath", label="Upload medical image (X-ray, etc.)")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio(label="Voice of the Doctor")
    ],
    title="🧠 AI Doctor: Voice + Vision Diagnosis",
    description="Speak your symptoms and upload a medical image. Get advice back — like a virtual doctor."
)

# Run with production settings for Render
iface.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))


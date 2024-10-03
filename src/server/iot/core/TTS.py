
import os
from typing import IO
from io import BytesIO
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

def text_to_speech_stream(text: str) -> IO[bytes]:
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    client = ElevenLabs(
        api_key=ELEVENLABS_API_KEY,
    )
    # Perform the text-to-speech conversion
    response = client.text_to_speech.convert(
        voice_id="EfztNqUsXD1wre8Wij7O", 
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_multilingual_v2",
        voice_settings=VoiceSettings(
            stability=0.75,
            similarity_boost=0.75,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    # Create a BytesIO object to hold the audio data in memory
    audio_stream = BytesIO()

    # Write each chunk of audio data to the stream
    for chunk in response:
        if chunk:
            audio_stream.write(chunk)

    # Reset stream position to the beginning
    audio_stream.seek(0)

    # Return the stream for further use
    return audio_stream


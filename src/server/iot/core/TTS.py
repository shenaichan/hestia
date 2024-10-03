
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

'''
  For more samples please visit https://github.com/Azure-Samples/cognitive-services-speech-sdk 
'''

import azure.cognitiveservices.speech as speechsdk
import os

def azure_tts(text):
    speech_config = speechsdk.SpeechConfig(subscription=os.getenv("AZURE_STT_ACCESS_KEY"), region="eastus")
    # Note: the voice setting will not overwrite the voice element in input SSML.
    speech_config.speech_synthesis_voice_name = "en-US-CoraMultilingualNeural"

    # text = "Hi, this is Cora Multilingual"

    # use the default speaker as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    result = speech_synthesizer.speak_text_async(text).get()
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))




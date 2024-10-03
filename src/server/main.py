import pvporcupine
import os
import pyaudio
import struct
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
import paho.mqtt.client as mqtt
from pathlib import Path
from core.STT import recognize_from_microphone
from core.TTS import azure_tts
# from core.audio_out import play_audio_with_pyaudio
from core.function_routing import answer
# from core.play_ding import play_ding
from apis.spotify_api import play_artist
import platform
import json

import pyaudio
import wave

# import pygame



# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc, properties):
    print("Connected with result code " + str(rc))
    client.subscribe("test/to_main")

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

# MQTT
client = None

# load env variables
load_dotenv(find_dotenv())

# for staggering keyword recognition
prev_time = datetime.now()

# params for porcupine initializer
access_key = os.getenv('PV_ACCESS_KEY')
base_path = Path(__file__).resolve().parent.parent.parent

keyword_paths = []
if platform.system() == "Darwin":
    keyword_paths=[base_path / 'wake_word_models/hestia_MAC.ppn', 
                   base_path / 'wake_word_models/hey_hestia_MAC.ppn']
else:
    keyword_paths=[base_path / 'wake_word_models/hestia_rpi.ppn', 
                   base_path / 'wake_word_models/hey_hestia_rpi.ppn']

# create objects to be populated later, if fail then they're available to be handled in the finally case
porcupine = None
audio_stream = None
pa = None

# debug var
cnt = 0

try:

    # # Create an MQTT client instance
    # client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    # # Assign the callback functions
    # client.on_connect = on_connect
    # client.on_message = on_message

    # # Connect to the local broker
    # client.connect("localhost", 1883, 60)

    # client.loop_start()

    # pygame.mixer.init()
    # pygame.mixer.music.load("ding.mp3")

    # Initialize the Porcupine object
    porcupine = pvporcupine.create(
        access_key=access_key,
        keyword_paths=keyword_paths
    )

    # Initialize PyAudio
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length 
    )

    print("Listening for wake word...")

    while True:
        pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
        # decode pcm into frame_length 16bit signed shorts
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)
        
        if keyword_index >= 0 and (datetime.now() - prev_time).seconds >= 1:
            audio_stream.stop_stream()
            prev_time = datetime.now()
            # client.publish("test/from_main", "hestia listening")
            if keyword_index == 0:
                cnt += 1
                print(str(cnt) + " hestia detected!")
            elif keyword_index == 1:
                cnt += 1
                print(str(cnt) + " hey hestia detected!")

            # pygame.mixer.music.play()
            # while pygame.mixer.music.get_busy():
            #     pygame.time.Clock().tick(10)
            azure_tts("what's up?")
                
            user_text = recognize_from_microphone()

            azure_tts("sure! let me think")

            if user_text:
                response = answer(user_text)

                # Check if the model has made a tool_call. This is the case either if the "finish_reason" is "tool_calls" or if the "finish_reason" is "stop" and our API request had forced a function call
                if (response.choices[0].finish_reason == "tool_calls"):
                    # This handles the edge case where if we forced the model to call one of our functions, the finish_reason will actually be "stop" instead of "tool_calls"
                    # (our_api_request_forced_a_tool_call and response['choices'][0]['message']['finish_reason'] == "stop")):

                    # Handle tool call
                    print("Model made a tool call.")
                    # Your code to handle tool calls
                    # handle_tool_call(response)

                    print(response.choices[0])
                    tool_call = response.choices[0].message.tool_calls[0]
                    arguments = json.loads(tool_call.function.arguments)

                    artist = arguments.get('artist')
                    play_artist(artist)
                    azure_tts(f"Playing {artist}")
                    
                # Else finish_reason is "stop", in which case the model was just responding directly to the user
                elif response.choices[0].finish_reason == "stop":
                    # Handle the normal stop case
                    print("Model responded directly to the user.")
                    # Your code to handle normal responses
                    # handle_normal_response(response)
                    azure_tts(response.choices[0].message.content)

                # Catch any other case, this is unexpected
                else:
                    print("what")
            audio_stream.start_stream()

except KeyboardInterrupt:
    print("Stopping wake word detection")

finally:
    # Ensure resources are cleaned up
    if porcupine is not None:
        porcupine.delete()
    if audio_stream is not None:
        audio_stream.close()
    if pa is not None:
        pa.terminate()
    if client is not None:
        client.loop_stop()


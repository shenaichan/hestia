import os
from dotenv import load_dotenv, find_dotenv
import platform

import pvporcupine as wake_word
import pyaudio
import struct

import paho.mqtt.client as mqtt

from speech.STT import transcribe
from speech.TTS import synthesize

from llm.function_routing import answer_and_execute
import json

from pprint import pprint


# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc, properties):
    print("Connected with result code " + str(rc))
    # client.subscribe("commands")

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

# MQTT
client = None

# load env variables
load_dotenv(find_dotenv())

# params for porcupine initializer
access_key = os.getenv('PV_ACCESS_KEY')

keyword_paths = []
if platform.system() == "Darwin":
    keyword_paths=[
                    # 'assets/wake_word_models/hestia_MAC.ppn', 
                   'assets/wake_word_models/hey_hestia_MAC.ppn'
                  ]
else:
    keyword_paths=[
                    # 'assets/wake_word_models/hestia_rpi.ppn', 
                   'assets/wake_word_models/hey_hestia_rpi.ppn'
                  ]

porcupine = None
audio_stream = None
pa = None

try:

    # Create an MQTT client instance
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    # Assign the callback functions
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the local broker
    client.connect("10.0.0.244", 1883, 60)

    client.loop_start()

    porcupine = wake_word.create(
        access_key=access_key,
        keyword_paths=keyword_paths
    )

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
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
        keyword_index = porcupine.process(pcm)
        
        if keyword_index >= 0:

            audio_stream.stop_stream()
            print("hey hestia detected!")

            synthesize("what's up?")
            user_text = transcribe()

            if user_text:
                client.publish("commands", user_text)
                synthesize("sure! let me think")
                response = answer_and_execute(user_text)
                client.publish("responses", response)
                synthesize(response)

            else:
                synthesize("sorry. I didn't catch that")

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


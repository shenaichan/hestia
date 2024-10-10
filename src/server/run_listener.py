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



load_dotenv(find_dotenv())



wake_word_access_key = os.getenv('WAKE_WORD_ACCESS_KEY')
wake_word_paths = []
if platform.system() == "Darwin":
    wake_word_paths=['assets/wake_word_models/hey_hestia_MAC.ppn']
else:
    wake_word_paths=['assets/wake_word_models/hey_hestia_rpi.ppn']
wake_word_detector = wake_word.create(
    access_key=wake_word_access_key,
    keyword_paths=wake_word_paths
)



audio_connection = pyaudio.PyAudio()
listener = audio_connection.open(
    rate=wake_word_detector.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=wake_word_detector.frame_length 
)



def mqtt_on_connect(client, userdata, flags, rc, properties):
    print("Connected with result code " + str(rc))
    client.subscribe("ring timer")

def mqtt_on_message(client, userdata, msg):
    if msg.topic == "ring timer":
        timer_name = msg.payload.decode('utf-8')
        response = f"Your {timer_name} timer is finished."
        synthesize(response)
        client.publish("responses", response)

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_connect = mqtt_on_connect
mqtt_client.on_message = mqtt_on_message
mqtt_client.connect("10.0.0.244", 1883, 60)
mqtt_client.loop_start()



print("Listening for wake word...")



try:
    while True:
        curr_audio_frame = listener.read(wake_word_detector.frame_length, exception_on_overflow=False)
        curr_audio_frame = struct.unpack_from("h" * wake_word_detector.frame_length, curr_audio_frame)
        wake_word_is_present = wake_word_detector.process(curr_audio_frame)
        
        if wake_word_is_present >= 0:

            listener.stop_stream()
            print("hey hestia detected!")

            synthesize("what's up?")
            user_text = transcribe()

            if user_text:
                mqtt_client.publish("commands", user_text)
                synthesize("sure! let me think")
                response = answer_and_execute(user_text)
                mqtt_client.publish("responses", response)
                synthesize(response)

            else:
                synthesize("sorry. I didn't catch that")

            listener.start_stream()

except KeyboardInterrupt:
    print("Stopping listener process")

finally:
    wake_word_detector.delete()
    listener.close()
    audio_connection.terminate()
    mqtt_client.loop_stop()


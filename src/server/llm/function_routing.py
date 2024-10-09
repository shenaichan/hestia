from openai import OpenAI
import json
from apis.spotify_api import play_music, pause_music
import paho.mqtt.client as mqtt

tools = [
    {
        "type": "function",
        "function": {
            "name": "play_music",
            "description": "Play music on Spotify. Call this whenever a user wants to hear a specific song, or a musical artist, or an album, for example, when a user says 'Play Taylor Swift'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The song, artist, or album the user wants to listen to.",
                    },
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "pause_music",
            "description": "Pause music on Spotify. Call this whenever a user wants to pause playback, for example, when a user says 'Pause'.",
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_timer",
            "description": "Set an optionally named timer. Call this whenever a user wants to set a timer, for example, when a user says 'Set a spaghetti timer for 10 minutes' or 'Set a timer for 1 hour and 5 seconds'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "hours": {
                        "type": "number",
                        "description": "The number of hours on the timer.",
                    },
                    "minutes": {
                        "type": "number",
                        "description": "The number of minutes on the timer.",
                    },
                    "seconds": {
                        "type": "number",
                        "description": "The number of seconds on the timer.",
                    },
                    "name": {
                        "type": "string",
                        "description": "The name of the timer.",
                    },
                },
                "required": ["hours", "minutes", "seconds"],
                "additionalProperties": False,
            },
        }
    },
]

def answer_and_execute(text: str) -> str:

    if len(text) > 0 and text[-1] != ".":
        text += "."
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful home assistant."},
            {
                "role": "user",
                "content": text + " Answer in one sentence."
            }
        ],
        tools=tools,
    )

    # Check if the model has made a tool_call. This is the case either if the "finish_reason" is "tool_calls" or if the "finish_reason" is "stop" and our API request had forced a function call
    if response.choices[0].finish_reason == "tool_calls":

        print("Model made a tool call.")

        tool_call = response.choices[0].message.tool_calls[0]
        function_name = tool_call.function.name
        status = ""
        if function_name == "create_timer":
            mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
            mqtt_client.connect("10.0.0.244", 1883, 60)
            mqtt_client.loop_start()
            mqtt_client.publish("set timer", tool_call.function.arguments)
            mqtt_client.loop_stop()
            status = "Timer set."
        else:
            arguments = json.loads(tool_call.function.arguments)
            status = globals()[function_name](**arguments)

        return status
        
    # Else finish_reason is "stop", in which case the model was just responding directly to the user
    elif response.choices[0].finish_reason == "stop":
        print("Model responded directly to the user.")
        return response.choices[0].message.content
    
    else:
        return "sorry. something went wrong"

from openai import OpenAI
import json
from apis.spotify_api import play_music, pause_music

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
]

def answer_and_execute(text: str) -> str:
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
        arguments = json.loads(tool_call.function.arguments)

        status = globals()[function_name](**arguments)

        return status
        
    # Else finish_reason is "stop", in which case the model was just responding directly to the user
    elif response.choices[0].finish_reason == "stop":
        print("Model responded directly to the user.")
        return response.choices[0].message.content
    
    else:
        return "sorry. something went wrong"

from openai import OpenAI

tools = [
    {
        "type": "function",
        "function": {
            "name": "play_artist",
            "description": "Play a musical artist on Spotify. Call this whenever a user wants to hear a musical artist, for example, when a user says 'Play Taylor Swift'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "artist": {
                        "type": "string",
                        "description": "The musical artist's name.",
                    },
                },
                "required": ["artist"],
                "additionalProperties": False,
            },
        }
    }
]

def answer(text: str) -> str:
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": text + " Answer in one sentence."
            }
        ],
        tools=tools,
    )

    '''
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
        synthesize(f"Playing {artist}")
        
    # Else finish_reason is "stop", in which case the model was just responding directly to the user
    elif response.choices[0].finish_reason == "stop":
        print("Model responded directly to the user.")
        synthesize(response.choices[0].message.content)

    # Catch any other case, this is unexpected
    else:
        print("what")
    '''

    return completion

    # print(completion.choices[0].message.content)
    # return completion.choices[0].message.content
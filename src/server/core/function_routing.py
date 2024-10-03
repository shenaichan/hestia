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

def answer(text: str):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": text + " Answer in one sentence."
            }
        ],
        tools=tools,
    )

    return completion

    # print(completion.choices[0].message.content)
    # return completion.choices[0].message.content
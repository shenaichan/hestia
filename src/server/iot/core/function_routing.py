from openai import OpenAI

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
        ]
    )

    print(completion.choices[0].message.content)
    return completion.choices[0].message.content
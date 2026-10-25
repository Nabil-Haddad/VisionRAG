from anthropic import Anthropic
from src.config import ANTHROPIC_API_KEY, DEFAULT_MODEL


def text_generation():
    # Initialise the client using the api key
    client = Anthropic(api_key= ANTHROPIC_API_KEY)
    # Create the messages
    message = client.messages.create(
        model= DEFAULT_MODEL,
        max_tokens=1024,
        messages=[
            {
            "role": "user",
            "content": "Hello Claude!",
            }
        ],
    )

    for block in message.content:
        if block.type == "text":
            print(block.text)




if __name__ == "__main__":
    text_generation()
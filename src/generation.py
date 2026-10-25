from anthropic import Anthropic
from config import ANTHROPIC_API_KEY, DEFAULT_MODEL, MEDIA_TYPE, gets_all_images
import os
import base64
import mimetypes

def text_generation(content):
    # Initialise the client using the api key
    client = Anthropic(api_key= ANTHROPIC_API_KEY)
    # Create the messages
    message = client.messages.create(
        model= DEFAULT_MODEL,
        max_tokens=1024,
        messages=[
            {
            "role": "user",
            "content": content,
            }
        ],
    )

    for block in message.content:
        if block.type == "text":
            print(block.text)



def image_describe_generation(image_file, content, type):
    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(
        model=DEFAULT_MODEL,
        max_tokens= 1024,
        messages=[
            {
                "role" : "user",
                "content" : [
                    {
                        "type" : "image",
                        "source" : {
                            'type' : 'base64',
                            'media_type' : type,
                            'data': image_file
                        },
                    },
                    {
                        "type": "text",
                        "text" : content
                    }
                ]
            },
        ]
    )

    for block in message.content:
        if block.type == "text":
            print(block.text)

def get_image_ready(image_name:str , image_folder:str , prompts : list[str]):
    image_path = os.path.join(image_folder, image_name)

    if not os.path.exists(image_path):
        print(f"Error: Could not find the image at '{image_path}'. Check your folder and filename.")
        exit()

    media_type = mimetypes.guess_type(image_path)[0] 
    with open(image_path, "rb") as image_file:
        binary_data = image_file.read()
        base64_image = base64.b64encode(binary_data).decode("utf-8")


        for prompt in prompts:
            image_describe_generation(base64_image, prompt , media_type)


if __name__ == "__main__":
    # text_generation('what is 2 + 2')
    images = gets_all_images()
    prompts = [
        [
            "Describe this image.",
            "List every distinct object you can see, one per line."
        ],
        [
            "How many wine glasses are in this image",
            "What is the type of the bottle on the left"
        ],
        [
            "Transcribe all visible text exactly as written.",
            "Transcribe all visible text, and tell me which parts you are unsure about."
        ]
    ]

    for image, image_prompts in zip(images, prompts):
        print(f"\n=== {image['image']} ===")
        get_image_ready(image["image"], image["image_folder"], image_prompts)




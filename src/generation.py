from anthropic import Anthropic
from config import ANTHROPIC_API_KEY, DEFAULT_MODEL, gets_all_images


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

def image_describe_generation(image, image_label, content):
    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(
        model=DEFAULT_MODEL,
        messages=[
            {},
        ]
    )
    pass


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

    test_array = []
    test_dict = {}
    for image , prompt in zip(images , prompts):
        list_images = list(image)
        test_dict["image"] = list_images[0]
        test_dict["image_folder"] = list_images[1]
        test_dict["prompts"] = prompt
        test_array.append(test_dict)


    print(test_array[0])



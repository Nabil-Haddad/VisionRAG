from anthropic import Anthropic
from config import ANTHROPIC_API_KEY, DEFAULT_MODEL, PROMPTS, gets_all_images
import os
import base64
import mimetypes
from utils.save_response import save_results_csv




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
    results = []
    for block in message.content:
        if block.type == "text":
            results.append(block.text)

    return results

def get_image_ready(image_name:str , image_folder:str , prompts : list[str]):
    image_path = os.path.join(image_folder, image_name)

    if not os.path.exists(image_path):
        print(f"Error: Could not find the image at '{image_path}'. Check your folder and filename.")
        exit()

    media_type = mimetypes.guess_type(image_path)[0] 
    with open(image_path, "rb") as image_file:
        binary_data = image_file.read()
        base64_image = base64.b64encode(binary_data).decode("utf-8")

        prompt_results = []
        for prompt in prompts:
            response = image_describe_generation(base64_image, prompt , media_type)
            prompt_results.append({
                "image": image_name,
                "prompt": prompt,
                "response": "\n".join(response),
            })

    return prompt_results
            
        


    


if __name__ == "__main__":
    # text_generation('what is 2 + 2')
    images = gets_all_images()
    
    final_output = []
    for image, image_prompts in zip(images, PROMPTS):
        print(f"\n=== {image['image']} ===")
        final_output.append(get_image_ready(image["image"], image["image_folder"], image_prompts))

    save_results_csv(final_output)
    # response_array = get_image_ready(images[0]["image"], images[0]["image_folder"], PROMPTS[0])
    # for r in response_array:
    #     print(r)


    



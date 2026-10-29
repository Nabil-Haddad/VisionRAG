import os
from dotenv import load_dotenv
from pathlib import Path
import logging

load_dotenv()

# Get the api key from .env
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Set up the default model
DEFAULT_MODEL = "claude-sonnet-5-5"

# Set the media type
MEDIA_TYPE = "jpg"

# Set the main directory path
BASE_DIR = Path(__file__).resolve().parent.parent

# add an assests directory

SHEETS_DIR = BASE_DIR / "assets" / "sheets"



PROMPTS = [
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



def gets_all_images(folder_path="data/images"):
    valid_extensions = (".jpg", ".jpeg", ".png", ".gif", ".webp")
    images_list = []

    if not os.path.exists(folder_path):
        raise ValueError(f"Their is no folder with such name {folder_path}")

    for filename in sorted(os.listdir(folder_path)):
        if filename.lower().endswith(valid_extensions):
            images_list.append({"image": filename, "image_folder": folder_path})

    return images_list


if __name__ == "__main__":
    print(gets_all_images())
    print(BASE_DIR)
    print(SHEETS_DIR)
    
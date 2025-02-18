import os
import requests
from dotenv import load_dotenv

from unstract.llmwhisperer import LLMWhispererClientV2
from google import genai

from backend.models.reciepts import Reciepts

load_dotenv()

LLMWHISPERER_API_KEY = os.getenv("LLMWHISPERER_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def convert_receipt_to_text(image_path: str):
    clientllm = LLMWhispererClientV2(
        base_url="https://llmwhisperer-api.us-central.unstract.com/api/v2",
        api_key=LLMWHISPERER_API_KEY,
        logging_level="INFO",
    )
    whisper = clientllm.whisper(
        file_path=image_path, wait_for_completion=True, wait_timeout=200
    )
    output = whisper["extraction"]["result_text"]
    return output


def convert_text_to_json(output: str):
    client = genai.Client(api_key=GEMINI_API_KEY)
    data = "convert this to json." + output
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=data,
        config={
            "response_mime_type": "application/json",
            "response_schema": Reciepts,
        },
    )
    final_lineitems = response.parsed

    return final_lineitems


def download_image(url, folder="bills", filename="downloaded_image.jpg"):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Get the image data
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        image_path = os.path.join(folder, filename)
        with open(image_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Image downloaded successfully: {image_path}")
    else:
        print("Failed to download image. Check the URL.")

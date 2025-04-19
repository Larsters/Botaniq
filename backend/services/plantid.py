import base64
import os
import requests
from dotenv import load_dotenv

load_dotenv()
PLANTID_API_KEY = os.getenv("PLANTID_API_KEY")

def identify_plant(image_path):
    url = "https://plant.id/api/v3/identification"
    with open(image_path, "rb") as file:
        encoded_image = base64.b64encode(file.read()).decode("utf-8")
    payload = {
        "images": [encoded_image],
        "organs": ["leaf", "flower"],
        "similar_images": True
    }
    headers = {
        "Content-Type": "application/json",
        "Api-Key": PLANTID_API_KEY,
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

def get_identification_results(request_id):
    details = "common_names, url, description, taxonomy, rank, gbif_id, inaturalist_id, image, synonyms, edible_parts, watering"
    url = f"https://plant.id/api/v3/identification/{request_id}?details={details}&language=en"

    header = {
        "Api-Key": PLANTID_API_KEY,
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=header)
    response.raise_for_status()
    return response.json()
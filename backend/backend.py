
import os
import json
DATASET_PATH = os.path.join(os.path.dirname(__file__), 'dataset.json')

def get_recommendations(plant_type, soil_type=None, soil_ph=None, lat=None, lon=None):
    with open(DATASET_PATH, 'r') as file:
        dataset = json.load(file)
    plant_type = plant_type.lower()
    if plant_type not in dataset:
        return "Sorry, I don't have recommendations for that plant yet."

    data = dataset[plant_type]
    rec = (
        f"🌱 Recommendations for {plant_type.capitalize()}:\n"
        f"- Water every {data['watering_frequency_days']} days\n"
        f"- Ideal pH: {data['ideal_ph'][0]}–{data['ideal_ph'][1]}\n"
        f"- Recommended fertilizer: {data['fertilizer']}\n"
        f"- Optimal temperature: {data['temperature_range_celsius'][0]}–{data['temperature_range_celsius'][1]}°C\n"
    )

    # Soil type feedback
    if soil_type:
        rec += f"\nYour soil type: {soil_type}."
        if plant_type == "cannabis" and soil_type.lower() != "loamy":
            rec += " For best results, Cannabis prefers loamy soil."
        elif plant_type == "basil" and soil_type.lower() != "sandy loam":
            rec += " Basil grows best in sandy loam soil."

    # Soil pH feedback
    if soil_ph:
        ideal_min, ideal_max = data["ideal_ph"]
        rec += f"\nYour soil pH: {soil_ph}."
        if not (ideal_min <= soil_ph <= ideal_max):
            rec += f" Adjust your soil pH to be between {ideal_min} and {ideal_max} for optimal growth."

    return rec
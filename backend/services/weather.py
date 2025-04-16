import requests
import os
from dotenv import load_dotenv

load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_current_weather(lat, lon):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={lat}&lon={lon}&units=metric&appid={OPENWEATHER_API_KEY}"
    )
    response = requests.get(url)
    return response.json()

def get_forecast_weather(lat, lon):
    url = (
        f"https://api.openweathermap.org/data/2.5/forecast?"
        f"lat={lat}&lon={lon}&units=metric&appid={OPENWEATHER_API_KEY}"
    )
    response = requests.get(url)
    return response.json()

# Optional: historical (requires paid plan)

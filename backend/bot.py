from dotenv import load_dotenv
import os
import requests
from telegram import ReplyKeyboardMarkup, Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler, MessageHandler, filters
from services.plantid import get_identification_results, identify_plant
from services.weather import get_current_weather, get_soil_data
from misc import user_data, user_location
from data.connect import insert_or_update_user, insert_farm, insert_plant
from shared import user_waiting_for_plant

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    keyboard = [[KeyboardButton("Send Location", request_location=True)]]
    await update.message.reply_text(
        "🌱 Welcome to Botaniq SmartGrow!\nSend your location so I can give you plant care advice.",
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# handles location messages
async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    username = update.effective_user.username
    location = update.message.location
    lat, lon = location.latitude, location.longitude

    # 1. Insert or update user
    insert_or_update_user(user_id, username)

    # 2. Get weather and soil data
    weather = get_current_weather(lat, lon)
    temp = weather["main"]["temp"]
    humidity = weather["main"]["humidity"]
    description = weather["weather"][0]["description"]
    soil_data = get_soil_data(lat, lon)
    soil_type = soil_data.get("properties", {}).get("most_probable_soil_type", "Unknown")
    soil_ph = soil_data.get("properties", {}).get("ph", None)

    # 3. Insert new farm (for demo, name is "My Farm", you can prompt for a name)
    farm_id = insert_farm(user_id, name="My Farm", latitude=lat, longitude=lon, soil_type=soil_type, soil_ph=soil_ph)

    await update.message.reply_text(
        f"Location received: {lat}, {lon}"
        f"\nCurrent weather: {description}, "
        f"Temperature: {temp}°C, Humidity: {humidity}%"
        f"\nMost probable soil type: {soil_type}"
    )

    # 4. Prompt for plant type
    plant_keyboard = [
        [KeyboardButton("Beans"), KeyboardButton("Cannabis")],
        [KeyboardButton("Basil"), KeyboardButton("Other")]
    ]
    await update.message.reply_text(
        "Please select the plant type:",
        reply_markup=ReplyKeyboardMarkup(plant_keyboard, resize_keyboard=True)
    )
    user_waiting_for_plant[user_id] = farm_id


    

async def set_plant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if context.args:
        plant_type = context.args[0].lower()
        if user_id in user_data:
            user_data[user_id]["plant"] = plant_type
        else:
            user_data[user_id] = {"plant": plant_type, "lat": None, "lon": None}
        await update.message.reply_text(f"Plant type set to: {plant_type}")
    else:
        user_waiting_for_plant.add(user_id)
        await update.message.reply_text("Please type the plant type (e.g. tomatoes):")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip().lower()
    known_plants = ["beans", "basil", "cannabis"]

    if user_id in user_waiting_for_plant:
        farm_id = user_waiting_for_plant.pop(user_id)
        if text in known_plants:
            insert_plant(farm_id, plant_type=text, last_temperature=None)
            await update.message.reply_text(f"✅ Plant '{text.capitalize()}' added to your farm!")
        elif text == "other":
            user_waiting_for_plant[user_id] = farm_id
            await update.message.reply_text(
                "Please send a clear photo of your plant for identification."
            )
        else:
            await update.message.reply_text(
                "Unknown plant type. Please choose Beans, Basil, Cannabis, or Other."
            )
    else:
        await update.message.reply_text("Please send your location first.")

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in user_waiting_for_plant:
        await update.message.reply_text("Please send your location and select 'Other' first.")
        return

    farm_id = user_waiting_for_plant.pop(user_id)
    photo_file = await update.message.photo[-1].get_file()
    file_path = f"tmp/{user_id}.jpg"
    await photo_file.download_to_drive(file_path)

    try:
        identification_result = identify_plant(file_path)
        # Extract plant name from identification_result as before
        suggestions = identification_result.get("result", {}).get("classification", {}).get("suggestions", [])
        if suggestions:
            top_suggestion = suggestions[0]
            plant_name = top_suggestion.get("name")
            insert_plant(farm_id, plant_type=plant_name, last_temperature=None)
            await update.message.reply_text(
                f"✅ Plant '{plant_name.capitalize()}' identified and added to your farm!"
            )
        else:
            await update.message.reply_text("❌ Could not clearly identify your plant. Please try again with a different image.")
    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"❌ API error: {e}")

# set up app
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.LOCATION, handle_location))
app.add_handler(CommandHandler("set_plant", set_plant))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.add_handler(MessageHandler(filters.PHOTO, handle_image))


if __name__ == "__main__":
    app.run_polling()

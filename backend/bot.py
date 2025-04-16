from dotenv import load_dotenv
import os
from telegram import ReplyKeyboardMarkup, Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler, MessageHandler, filters
from services.weather import get_current_weather, get_soil_data
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# while no db, store user location in memory
user_location = {}

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
    location = update.message.location
    lat, lon = location.latitude, location.longitude
    user_location[user_id] = (lat, lon)
    weather = get_current_weather(lat, lon)
    temp = weather["main"]["temp"]
    humidity = weather["main"]["humidity"]
    description = weather["weather"][0]["description"]
    soil_data = get_soil_data(lat, lon)
    soil_type = soil_data.get("properties", {}).get("most_probable_soil_type", "Unknown")
    await update.message.reply_text(f"Location received: {lat}, {lon}"
                                    f"\nCurrent weather: {description}, "
                                    f"Temperature: {temp}°C, Humidity: {humidity}% "
                                    f"With the most probable soil type: {soil_type}"     
                                    )

# set up app
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.LOCATION, handle_location))



if __name__ == "__main__":
    app.run_polling()

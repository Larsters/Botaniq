from telegram import Update
from telegram.ext import ContextTypes
from shared import user_waiting_for_plant

from backend import get_recommendations
from data.connect import insert_plant

# while no db, store user location in memory
user_location = {}
user_data = {}

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip().lower()
    if user_id in user_waiting_for_plant:
        farm_id = user_waiting_for_plant.pop(user_id)
        insert_plant(farm_id, plant_type=text, last_temperature=None)
        await update.message.reply_text(f"✅ Plant '{text.capitalize()}' added to your farm!")
    else:
        await update.message.reply_text("Please send your location first.")
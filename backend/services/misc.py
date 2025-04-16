from telegram import Update
from telegram.ext import ContextTypes

# while no db, store user location in memory
user_location = {}
user_data = {}
user_waiting_for_plant = set()

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages."""
    user_id = update.message.from_user.id
    if user_id in user_waiting_for_plant:
        plant_type = update.message.text.lower()
        if user_id in user_data:
            user_data[user_id]["plant"] = plant_type
        else:
            user_data[user_id] = {"plant": plant_type, "lat": None, "lon": None}
        user_waiting_for_plant.discard(user_id)
        await update.message.reply_text(f"Plant type set to: {plant_type}")